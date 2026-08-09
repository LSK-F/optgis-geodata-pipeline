# ==============================================================================
# Setup Script - R Dependencies Installation
# ==============================================================================

message("Starting R packages verification...")

required_packages <- c("geocodebr", "sf")

installed_packages <- installed.packages()[,"Package"]
missing_packages <- required_packages[!(required_packages %in% installed_packages)]

if (length(missing_packages) > 0) 
{
  message("Installing missing packages: ", paste(missing_packages, collapse = ", "))
  install.packages(missing_packages, dependencies = TRUE, repos = "https://cloud.r-project.org")
  message("Installation successfully completed!")
} else {
  message("All required packages are already installed.")
}