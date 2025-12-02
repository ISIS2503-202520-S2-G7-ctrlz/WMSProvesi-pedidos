# ***************** Universidad de los Andes ***********************
# ****** Departamento de Ingeniería de Sistemas y Computación ******
# ********** Arquitectura y diseño de Software - ISIS2503 **********
#
# Infraestructura para laboratorio de Microservicios - WMSProvesi
#
# Elementos a desplegar en AWS:
# 1. Grupos de seguridad:
#    - <prefix>-traffic-api   (puerto 8000 - Kong)
#    - <prefix>-traffic-apps  (puerto 8080 - microservicios)
#    - <prefix>-traffic-db    (puerto 5432 - PostgreSQL)
#    - <prefix>-traffic-ssh   (puerto 22 - SSH)
#    - <prefix>-traffic-front (puerto 5173 - Vite)
#
# 2. Instancias EC2:
#    - <prefix>-pedidos-db   (PostgreSQL en Docker)
#    - <prefix>-productos-db (PostgreSQL en Docker)
#    - <prefix>-bodegas-db   (PostgreSQL en Docker)
#
#    - <prefix>-pedidos-ms   (microservicio Pedidos)
#    - <prefix>-productos-ms (microservicio Productos)
#    - <prefix>-bodegas-ms   (microservicio Bodegas)
#    - <prefix>-front-ms     (Front React/Vite)
#
#    - <prefix>-kong         (Kong API Gateway)
# ******************************************************************

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.18.0"
    }
  }
}

variable "region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "project_prefix" {
  description = "Prefix used for naming AWS resources"
  type        = string
  default     = "wms"
}

variable "instance_type" {
  description = "EC2 instance type for application hosts"
  type        = string
  default     = "t3.micro"
}

provider "aws" {
  region = var.region
}

locals {
  project_name = "${var.project_prefix}-microservices"
  repository   = "https://github.com/ISIS2503-202520-S2-G7-ctrlz/WMSProvesi-pedidos.git"

  common_tags = {
    Project   = local.project_name
    ManagedBy = "Terraform"
  }
}

# Ubuntu 24.04 para las instancias que corren Python/Django/Node
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# -----------------------------------------------------------------
# Grupos de seguridad
# -----------------------------------------------------------------

resource "aws_security_group" "traffic_api" {
  name        = "${var.project_prefix}-traffic-api"
  description = "Allow API Gateway traffic on port 8000"

  ingress {
    description = "HTTP access for gateway layer"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-api"
  })
}

resource "aws_security_group" "traffic_apps" {
  name        = "${var.project_prefix}-traffic-apps"
  description = "Allow microservices traffic on port 8080"

  ingress {
    description = "HTTP access for microservices"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-apps"
  })
}

resource "aws_security_group" "traffic_db" {
  name        = "${var.project_prefix}-traffic-db"
  description = "Allow PostgreSQL access"

  ingress {
    description = "PostgreSQL from anywhere (solo laboratorio)"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-db"
  })
}

resource "aws_security_group" "traffic_ssh" {
  name        = "${var.project_prefix}-traffic-ssh"
  description = "Allow SSH access"

  ingress {
    description = "SSH access from anywhere (solo laboratorio)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-ssh"
  })
}

# Nuevo SG para el front Vite (5173)
resource "aws_security_group" "traffic_front" {
  name        = "${var.project_prefix}-traffic-front"
  description = "Allow Vite front traffic on port 5173"

  ingress {
    description = "Vite Dev Server"
    from_port   = 5173
    to_port     = 5173
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-front"
  })
}

# -----------------------------------------------------------------
# Bases de datos (PostgreSQL en Docker en Amazon Linux)
# -----------------------------------------------------------------

resource "aws_instance" "pedidos_db" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [
    aws_security_group.traffic_db.id,
    aws_security_group.traffic_ssh.id,
  ]

  user_data = <<-EOT
              #!/bin/bash
              docker run --restart=always -d \
                -e POSTGRES_USER=pedidos_user \
                -e POSTGRES_DB=pedidos_db \
                -e POSTGRES_PASSWORD=isis2503 \
                -p 5432:5432 \
                --name pedidos-db postgres
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-pedidos-db"
    Role = "pedidos-db"
  })
}

resource "aws_instance" "productos_db" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [
    aws_security_group.traffic_db.id,
    aws_security_group.traffic_ssh.id,
  ]

  user_data = <<-EOT
              #!/bin/bash
              docker run --restart=always -d \
                -e POSTGRES_USER=productos_user \
                -e POSTGRES_DB=productos_db \
                -e POSTGRES_PASSWORD=isis2503 \
                -p 5432:5432 \
                --name productos-db postgres
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-productos-db"
    Role = "productos-db"
  })
}

resource "aws_instance" "bodegas_db" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [
    aws_security_group.traffic_db.id,
    aws_security_group.traffic_ssh.id,
  ]

  user_data = <<-EOT
              #!/bin/bash
              docker run --restart=always -d \
                -e POSTGRES_USER=bodegas_user \
                -e POSTGRES_DB=bodegas_db \
                -e POSTGRES_PASSWORD=isis2503 \
                -p 5432:5432 \
                --name bodegas-db postgres
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-bodegas-db"
    Role = "bodegas-db"
  })
}

# -----------------------------------------------------------------
# Microservicios (Ubuntu + Django/DRF)
# -----------------------------------------------------------------

resource "aws_instance" "pedidos_ms" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [
    aws_security_group.traffic_apps.id,
    aws_security_group.traffic_ssh.id,
  ]

  user_data = <<-EOT
              #!/bin/bash

              export PEDIDOS_DB_HOST=${aws_instance.pedidos_db.private_ip}
              echo "PEDIDOS_DB_HOST=${aws_instance.pedidos_db.private_ip}" | sudo tee -a /etc/environment

              sudo apt-get update -y
              sudo apt-get install -y git python3-pip build-essential libpq-dev python3-dev

              mkdir -p /labs
              cd /labs

              if [ ! -d WMSProvesi-pedidos ]; then
                git clone ${local.repository}
              fi

              # Aquí puedes automatizar el arranque del ms de pedidos
              # cd WMSProvesi-pedidos
              # pip3 install -r requirements.txt
              # python3 manage.py migrate
              # python3 manage.py runserver 0.0.0.0:8080 &
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-pedidos-ms"
    Role = "pedidos-ms"
  })

  depends_on = [aws_instance.pedidos_db]
}

resource "aws_instance" "productos_ms" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [
    aws_security_group.traffic_apps.id,
    aws_security_group.traffic_ssh.id,
  ]

  user_data = <<-EOT
              #!/bin/bash

              export PRODUCTOS_DB_HOST=${aws_instance.productos_db.private_ip}
              echo "PRODUCTOS_DB_HOST=${aws_instance.productos_db.private_ip}" | sudo tee -a /etc/environment

              sudo apt-get update -y
              sudo apt-get install -y git python3-pip build-essential libpq-dev python3-dev

              mkdir -p /labs
              cd /labs

              if [ ! -d WMSProvesi-pedidos ]; then
                git clone ${local.repository}
              fi

              # TODO: automatizar el ms de productos (similar a pedidos)
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-productos-ms"
    Role = "productos-ms"
  })

  depends_on = [aws_instance.productos_db]
}

resource "aws_instance" "bodegas_ms" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [
    aws_security_group.traffic_apps.id,
    aws_security_group.traffic_ssh.id,
  ]

  user_data = <<-EOT
              #!/bin/bash

              export BODEGAS_DB_HOST=${aws_instance.bodegas_db.private_ip}
              echo "BODEGAS_DB_HOST=${aws_instance.bodegas_db.private_ip}" | sudo tee -a /etc/environment

              sudo apt-get update -y
              sudo apt-get install -y git python3-pip build-essential libpq-dev python3-dev

              mkdir -p /labs
              cd /labs

              if [ ! -d WMSProvesi-pedidos ]; then
                git clone ${local.repository}
              fi

              # TODO: automatizar el ms de bodegas
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-bodegas-ms"
    Role = "bodegas-ms"
  })

  depends_on = [aws_instance.bodegas_db]
}

# -----------------------------------------------------------------
# Frontend React/Vite (dev mode en 5173)
# -----------------------------------------------------------------

resource "aws_instance" "front_ms" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [
    aws_security_group.traffic_apps.id,
    aws_security_group.traffic_front.id,  # expone 5173
    aws_security_group.traffic_ssh.id,
  ]

  user_data = <<-EOT
              #!/bin/bash

              export PEDIDOS_HOST=${aws_instance.pedidos_ms.private_ip}
              export PRODUCTOS_HOST=${aws_instance.productos_ms.private_ip}
              export BODEGAS_HOST=${aws_instance.bodegas_ms.private_ip}

              echo "PEDIDOS_HOST=${aws_instance.pedidos_ms.private_ip}"   | sudo tee -a /etc/environment
              echo "PRODUCTOS_HOST=${aws_instance.productos_ms.private_ip}" | sudo tee -a /etc/environment
              echo "BODEGAS_HOST=${aws_instance.bodegas_ms.private_ip}"   | sudo tee -a /etc/environment

              sudo apt-get update -y
              sudo apt-get install -y git nodejs npm

              mkdir -p /labs
              cd /labs

              if [ ! -d WMSProvesi-pedidos ]; then
                git clone ${local.repository}
              fi

              # Ajusta esta ruta si tu front está en otra carpeta
              cd WMSProvesi-pedidos/front

              npm install

              # Vite dev server accesible desde fuera
              npm run dev -- --host 0.0.0.0 --port 5173 &
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-front-ms"
    Role = "front-ms"
  })

  depends_on = [
    aws_instance.pedidos_ms,
    aws_instance.productos_ms,
    aws_instance.bodegas_ms,
  ]
}

# -----------------------------------------------------------------
# Kong API Gateway
# -----------------------------------------------------------------

resource "aws_instance" "kong" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [
    aws_security_group.traffic_api.id,
    aws_security_group.traffic_ssh.id,
  ]

  user_data = <<-EOT
              #!/bin/bash

              export PEDIDOS_HOST=${aws_instance.pedidos_ms.private_ip}
              export PRODUCTOS_HOST=${aws_instance.productos_ms.private_ip}
              export BODEGAS_HOST=${aws_instance.bodegas_ms.private_ip}
              export FRONT_HOST=${aws_instance.front_ms.private_ip}

              echo "PEDIDOS_HOST=${aws_instance.pedidos_ms.private_ip}"   | sudo tee -a /etc/environment
              echo "PRODUCTOS_HOST=${aws_instance.productos_ms.private_ip}" | sudo tee -a /etc/environment
              echo "BODEGAS_HOST=${aws_instance.bodegas_ms.private_ip}"   | sudo tee -a /etc/environment
              echo "FRONT_HOST=${aws_instance.front_ms.private_ip}"       | sudo tee -a /etc/environment

              sudo dnf install -y git

              sudo mkdir -p /labs
              cd /labs

              if [ ! -d WMSProvesi-pedidos ]; then
                sudo git clone ${local.repository}
              fi

              cd WMSProvesi-pedidos

              # Debes crear un kong.yaml en el repo con:
              # <PEDIDOS_HOST>, <PRODUCTOS_HOST>, <BODEGAS_HOST>, <FRONT_HOST>
              if [ -f kong.yaml ]; then
                sudo sed -i "s/<PEDIDOS_HOST>/${aws_instance.pedidos_ms.private_ip}/g" kong.yaml
                sudo sed -i "s/<PRODUCTOS_HOST>/${aws_instance.productos_ms.private_ip}/g" kong.yaml
                sudo sed -i "s/<BODEGAS_HOST>/${aws_instance.bodegas_ms.private_ip}/g" kong.yaml
                sudo sed -i "s/<FRONT_HOST>/${aws_instance.front_ms.private_ip}/g" kong.yaml
              fi

              docker network create kong-net || true

              docker run -d --name kong --network=kong-net --restart=always \
                -v "$(pwd):/kong/declarative/" \
                -e "KONG_DATABASE=off" \
                -e "KONG_DECLARATIVE_CONFIG=/kong/declarative/kong.yaml" \
                -p 8000:8000 kong/kong-gateway
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-kong"
    Role = "api-gateway"
  })

  depends_on = [
    aws_instance.pedidos_ms,
    aws_instance.productos_ms,
    aws_instance.bodegas_ms,
    aws_instance.front_ms,
  ]
}

# -----------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------

output "kong_public_ip" {
  description = "Public IP for Kong API Gateway"
  value       = aws_instance.kong.public_ip
}

output "pedidos_ms_public_ip" {
  description = "Public IP for Pedidos MS"
  value       = aws_instance.pedidos_ms.public_ip
}

output "productos_ms_public_ip" {
  description = "Public IP for Productos MS"
  value       = aws_instance.productos_ms.public_ip
}

output "bodegas_ms_public_ip" {
  description = "Public IP for Bodegas MS"
  value       = aws_instance.bodegas_ms.public_ip
}

output "front_ms_public_url" {
  description = "URL del front Vite"
  value       = "http://${aws_instance.front_ms.public_ip}:5173"
}

output "pedidos_db_private_ip" {
  description = "Private IP for Pedidos DB"
  value       = aws_instance.pedidos_db.private_ip
}

output "productos_db_private_ip" {
  description = "Private IP for Productos DB"
  value       = aws_instance.productos_db.private_ip
}

output "bodegas_db_private_ip" {
  description = "Private IP for Bodegas DB"
  value       = aws_instance.bodegas_db.private_ip
}
