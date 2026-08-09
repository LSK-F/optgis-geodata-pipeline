# ==============================================================================
# Geocoding Pipeline - RJ School Census
# Developed by: Lucas J. S. Fernandes
# ==============================================================================

# Loading packages
library(geocodebr)
library(sf)
library(parallel)

options(timeout = 60*15)

input_path <- "./data/processed/censo_escolar_2024_RJ_Enderecos&Matriculas.csv"
output_path <- "./data/processed/censo_escolar_geocodificado.gpkg"

message("Starting to read the clean database...")
input_df <- read.csv(input_path, encoding = "UTF-8")

fields <- geocodebr::definir_campos(
  estado = "NO_UF",
  municipio = "NO_MUNICIPIO",
  logradouro = "DS_ENDERECO",
  numero = "NU_ENDERECO",
  cep = "CO_CEP",
  localidade = "NO_BAIRRO"
)


df_geocoded <- geocodebr::geocode(
  enderecos = input_df,
  campos_endereco = fields,
  resultado_completo = FALSE,
  resolver_empates = TRUE,
  resultado_sf = TRUE,       # TRUE to directly output ready spatial geometry
  verboso = TRUE,
  cache = TRUE,
  n_cores = 2 
)


message("Saving results in GeoPackage format...")
sf::st_write(df_geocoded, output_path, driver = "GPKG", append = FALSE)

message("Process finished successfully!")