output "ecs_cluster_name" {
  value = aws_ecs_cluster.card_search.name
}

output "ecs_service_name" {
  value = aws_ecs_service.card_search.name
}

output "ecs_service_security_group_id" {
  value = aws_security_group.ecs_service_sg.id
}

output "ecs_service_subnet_id" {
  value = aws_subnet.main.id
}

