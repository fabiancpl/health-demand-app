# Depuraci??n RUV --------------------------------------------------------------
# Descripcion: DModelos
# Author(s): AG
# input: Bases de datos de RUV
# output: .Rdata de bases de dato RUV
# File history:
#   201905215: creation

# Paths -------------------------------------------------------------------

rm(list =ls())

setwd("~/Desktop/DS4A/FinalProject")
input<- file.path("../input")
inputRUV <- file.path("~/Desktop/DS4A/FinalProject/files")

output <- file.path("../output/")
# Paquetes ----------------------------------------------------------------
library(dplyr) # #
library(tidyr)
library(openxlsx)
library(eeptools)
library(lubridate)
library(R.utils)
library(stringr)
library(sf)
library(tmap)
library(tmaptools)
library(leaflet)
library(stargazer)
require(ggplot2)
require(sandwich)
require(msm)
library(relaimpo)
library("mice") 
library(Hmisc)
library(jtools)



# Modelos
modelos = read.table(file = "./files/bdModelos.txt" , sep = "|")
modelos = modelos %>% 
  mutate(Sexo = as.character(Sexo)) %>% 
  mutate(Sexo = ifelse(Sexo %in% c('No Definido', 'No Reportado'), "No definido/No reportado", Sexo)) 

quantile(modelos$Total, prob=c(0,0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75,0.80, 0.90, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99,1))
inputData = modelos %>% 
  dplyr::select(Cerebro:IndAdultoMayor, CicloVida, GrupoEdad, Total) %>% 
  mutate(Total = ifelse(Total > 30, NA, Total)) %>% 
  mutate(Total1 = ceiling(Total))



# Gr??ficos

ggplot(inputData, aes(x=Etnia, y=Total, color = Etnia)) + 
  geom_violin(trim=FALSE) + 
  scale_color_brewer(palette="Paired")

# Mejor modelo lineal

modelo1 <- leaps::regsubsets(Total1~ Cerebro + 
                               Diabetes + 
                               Hipertension + 
                               Infarto + 
                               Mental + 
                               Tumor + 
                               factor(Sexo) + 
                               factor(Etnia) + 
                               IndDiscapacidad + 
                               IndAdultoMayor +
                               factor(CicloVida),  data = inputData, nbest=2)

plot(modelo1,scale="adjr2",  main = "Adjusted R^2 C14_0")
plot(modelo1,scale="bic",  main = "BIC C14_0")

lmMod1 <- lm(Total1 ~ Cerebro + 
               Diabetes + 
               Hipertension + 
               Infarto + 
               Mental + 
               Tumor + 
               factor(Sexo) + 
               factor(Etnia) + 
               IndDiscapacidad , data = inputData)
poissonM1 <- glm(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia + IndDiscapacidad , inputData, family = poisson(link = "log"))
poissonM2 <- glm(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia + IndDiscapacidad , inputData, family = quasipoisson(link = "log"))

stargazer(poissonM1, poissonM2, type="html", title = "",
          covariate.labels=c("Cerebrovascular",'Diabetes',"Hypertension","Heart attack",
                             "Mental", 'Tumor',"Sex(Men)", 'Sex(No defined)', 'NARP', 'No ethnicity', 'Rom (Gypsy)', 'Person with disability'),
          dep.var.labels=c("Number of demanded health services"), out = paste0("ModeloGeneral.htm"))

#negBinomial = glm.nb(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia + IndDiscapacidad, data = inputData, init.theta=1, link=identity, start=poissonM1$coef)
plot_summs(poissonM1, poissonM2,  
           coefs = c("Cerebrovascular" = "Cerebro", "Diabetes" = "Diabetes",
                     "Hypertension" = "Hipertension",
                     'Heart attack' = 'Infarto',
                     'Mental' = 'Mental', 
                     'Tumor' = 'Tumor',
                     'Men' = 'SexoMasculino',
                     'No defined sex' = 'SexoNo definido/No reportado',
                     'NARP' = 'EtniaNARP',
                     'No ethnicity' = 'EtniaNo aplica',
                     'Rom (Gypsy)' = 'EtniaRom (Gitano)',
                     'Person with disability'),scale = TRUE, exp = TRUE)

 # Grupo ??tnico -----------

inputData1 = modelos %>% 
  filter(IndEtnia == "Si") %>% 
  dplyr::select(Cerebro:IndAdultoMayor, CicloVida, GrupoEdad, Total) %>% 
  mutate(Total = ifelse(Total > 30, NA, Total)) %>% 
  mutate(Total1 = ceiling(Total))

poissonM1 <- glm(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia + IndDiscapacidad , inputData1, family = poisson(link = "log"))
poissonM2 <- glm(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia + IndDiscapacidad , inputData1, family = quasipoisson(link = "log"))


#negBinomial = glm.nb(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia + IndDiscapacidad, data = inputData, init.theta=1, link=identity, start=poissonM1$coef)
plot_summs(poissonM1, poissonM2,  
           coefs = c("Cerebrovascular" = "Cerebro", "Diabetes" = "Diabetes",
                     "Hypertension" = "Hipertension",
                     'Heart attack' = 'Infarto',
                     'Mental services' = 'Mental', 
                     'Tumor' = 'Tumor',
                     'Men' = 'SexoMasculino',
                     'No defined sex' = 'SexoNo definido/No reportado',
                     'NARP' = 'EtniaNARP',
                     'No ethnicity' = 'EtniaNo aplica',
                     'Rom (Gypsy)' = 'EtniaRom (Gitano)',
                     'Person with disability'),scale = TRUE, exp = TRUE)

# Grupo disability--------

inputData1 = modelos %>% 
  filter(IndDiscapacidad == "Si") %>% 
  dplyr::select(Cerebro:IndAdultoMayor, CicloVida, GrupoEdad, Total) %>% 
  mutate(Total = ifelse(Total > 30, NA, Total)) %>% 
  mutate(Total1 = ceiling(Total))

poissonM1 <- glm(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia  , inputData1, family = poisson(link = "log"))
poissonM2 <- glm(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia  , inputData1, family = quasipoisson(link = "log"))


#negBinomial = glm.nb(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia + IndDiscapacidad, data = inputData, init.theta=1, link=identity, start=poissonM1$coef)
plot_summs(poissonM1, poissonM2,  
           coefs = c("Cerebrovascular" = "Cerebro", "Diabetes" = "Diabetes",
                     "Hypertension" = "Hipertension",
                     'Heart attack' = 'Infarto',
                     'Mental services' = 'Mental', 
                     'Tumor' = 'Tumor',
                     'Men' = 'SexoMasculino',
                     'No defined sex' = 'SexoNo definido/No reportado',
                     'NARP' = 'EtniaNARP',
                     'No ethnicity' = 'EtniaNo aplica',
                     'Rom (Gypsy)' = 'EtniaRom (Gitano)'),scale = TRUE, exp = TRUE)

# Grupo Elderly -------

inputData1 = modelos %>% 
  filter(IndAdultoMayor == "Si") %>% 
  dplyr::select(Cerebro:IndAdultoMayor, CicloVida, GrupoEdad, Total) %>% 
  mutate(Total = ifelse(Total > 30, NA, Total)) %>% 
  mutate(Total1 = ceiling(Total))

poissonM1 <- glm(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia  +IndDiscapacidad , inputData1, family = poisson(link = "log"))
poissonM2 <- glm(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia  +IndDiscapacidad, inputData1, family = quasipoisson(link = "log"))


#negBinomial = glm.nb(Total1 ~ Cerebro + Diabetes + Hipertension + Infarto + Mental + Tumor + Sexo + Etnia + IndDiscapacidad, data = inputData, init.theta=1, link=identity, start=poissonM1$coef)
plot_summs(poissonM1, poissonM2,  
           coefs = c("Cerebrovascular" = "Cerebro", "Diabetes" = "Diabetes",
                     "Hypertension" = "Hipertension",
                     'Heart attack' = 'Infarto',
                     'Mental services' = 'Mental', 
                     'Tumor' = 'Tumor',
                     'Men' = 'SexoMasculino',
                     'No defined sex' = 'SexoNo definido/No reportado',
                     'NARP' = 'EtniaNARP',
                     'No ethnicity' = 'EtniaNo aplica',
                     'Rom (Gypsy)' = 'EtniaRom (Gitano)',
                     'Person with disability'),scale = TRUE, exp = TRUE)