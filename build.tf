data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/build/lambda"
  output_path = "${path.module}/build/${var.project_name}.zip"
  depends_on  = [null_resource.build_lambda]
}

data "archive_file" "layers_zip" {
  type        = "zip"
  source_dir  = "${path.module}/build/layers"
  output_path = "${path.module}/build/${var.project_name}-dependencies.zip"
  excludes    = ["__pycache__", "core/__pycache", "tests"]
  depends_on  = [null_resource.build_layers]
}

resource "null_resource" "build_lambda" {
  triggers = {
    src_directory_md5 = md5(join("", [for file in fileset("${path.module}/src", "*") : filemd5("${path.module}/src/${file}")]))
  }

  provisioner "local-exec" {
    command     = "scripts/build_lambda.sh"
    interpreter = ["/bin/bash", "-c"]
    working_dir = path.module
  }
}

resource "null_resource" "build_layers" {
  triggers = {
    pyproject_toml_md5 = filemd5("pyproject.toml")
  }

  provisioner "local-exec" {
    command     = "scripts/build_layers.sh"
    interpreter = ["/bin/bash", "-c"]
    working_dir = path.module
  }
}
