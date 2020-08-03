# Depuraci??n RUV --------------------------------------------------------------
# Descripcion: Depuraci??n bases de datos RUV
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
library(ggrepel)



# Functions ----------
# Loading RUV agregados ----------------

RUV = read.table(file = "./files/AgregaRUV.txt",sep = "|")

# Piramides poblacionales ---------------------

piramideInd <- RUV %>% 
  #filter(IndDiscapacidad == "Si") %>% 
  mutate(Poblacion = n) %>% 
  filter(Sexo %in% c("Femenino", "Masculino"))
popGH <- aggregate(formula = Poblacion ~ Sexo + GrupoEdad, data = piramideInd, FUN = sum)
popGH <- with(popGH, popGH[order(Sexo,GrupoEdad),])
popGH <- popGH[,c("GrupoEdad","Sexo","Poblacion")]

## barplots for male populations goes to the left (thus negative sign)
popGH$Poblacion <- ifelse(popGH$Sexo == "Masculino", -1*popGH$Poblacion, popGH$Poblacion)
popGH$label <- abs(popGH$Poblacion)
popGH$label2 <- round((popGH$label)/sum(popGH$label)*100, 1)
popGH$label1 <- paste(round((popGH$label)/sum(popGH$label)*100, 1), "%", sep = "")
popGH <- popGH %>% 
  mutate(GrupoEdad = factor(GrupoEdad, levels=c("[0,5)", "[5,10)", "[10,15)", "[15,20)", "[20,25)", "[25,30)", 
                                           "[30,35)", "[35,40)", '[40,45)', '[45,50)', '[50,55)',
                                           '[55,60)', '[60,65)', '[65,70)', '[70,75)', '[75,80)', '[80,85)',
                                           '[85,90)', '[90,95)', '[95,100]')))

## pyramid charts are two barcharts with axes flipped
ggplot(popGH, aes(x = GrupoEdad, y = Poblacion, fill = Sexo)) + 
  geom_bar(data = subset(popGH, Sexo != "Masculino"), stat = "identity") +
  geom_bar(data = subset(popGH, Sexo == "Masculino"), stat = "identity") + 
  #scale_y_continuous(labels = paste0(as.character(c(seq(2, 0, -1), seq(1, 2, 1))), "m")) + 
  coord_flip() +
  ggtitle("") +
  xlab("Age") + ylab("Percentage") + 
  theme_light() +
  geom_text(aes(label=label1), vjust = 0) +
  scale_fill_brewer(palette = "Pastel1")+
  theme(axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) 

ggsave("./graphs/piramEtnia.png", scale = 1.6, width = 4, height = 3)

# Etnia ------------------

etnia = RUV %>% 
  filter(IndEtnia == "Si") %>% 
  filter(Hecho == "Desplazamiento Forzado") %>% 
  mutate(Sexo = as.character(Sexo)) %>% 
  mutate(Sexo = ifelse(Sexo %in% c('No Definido', 'No Reportado'), "No definido/No reportado", Sexo)) %>% 
  group_by(Sexo, Etnia) %>% 
  summarise(n = sum(n))

ggplot(data=etnia, aes(x=Sexo, y=n, fill=Etnia)) +
  geom_bar(stat="identity", position=position_dodge())+
  geom_text(aes(label = format(n, big.mark = ".", scientific = FALSE)), vjust=-0.4, 
            position = position_dodge(0.9), size=3.5)+
  scale_fill_brewer(palette="Pastel1")+
  xlab("Sexo") + ylab("") + 
  theme(axis.text.x=element_blank(),
        axis.ticks.x=element_blank()) +
  theme_minimal()

ggsave("./graphs/Etnia.png", scale = 1.6, width = 4, height = 2.2)

# Hecho Victim ------------------

hecho = RUV %>% 
  filter(!Hecho %in% c("Desplazamiento Forzado", "Homicidio")) %>% 
  mutate(Sexo = as.character(Sexo)) %>% 
  mutate(Sexo = ifelse(Sexo %in% c('No Definido', 'No Reportado'), "No definido/No reportado", Sexo)) %>% 
  group_by(Sexo, Hecho) %>% 
  summarise(n = sum(n))
library(forcats)
ggplot(data=hecho, aes(x=fct_reorder(stringr::str_wrap(Hecho, 40), n), y=n, fill=Sexo)) +
  geom_bar(stat="identity", position=position_dodge())+
  geom_text(aes(label = format(n, big.mark = ".", scientific = FALSE)), vjust=-0.4, 
            position = position_dodge(0.9), size=3.5)+
  scale_fill_brewer(palette="Pastel1")+
  xlab("Hecho victimizante") + ylab("") + 
  theme_minimal() +
    theme(axis.title.x=element_blank(),
          axis.text.x=element_blank(),
          axis.ticks.x =element_blank())  +
   theme(axis.text.x = element_text(angle = 90))+
  coord_flip() 
 

ggsave("./graphs/Desplazamiento.png", scale = 1.6, width = 4, height = 2.2)

# Discapacidad ------------------

discapacCont = RUV %>% 
  group_by(IndDiscapacidad) %>% 
  summarise(n = sum(n)) %>% 
  ungroup() %>% 
  mutate(por = n/sum(n))

discapac = RUV %>% 
  filter(IndDiscapacidad == "Si") %>% 
  filter(!is.na(TipoAlteracion)) %>% 
 # filter(Hecho == "Desplazamiento Forzado") %>% 
  mutate(Sexo = as.character(Sexo)) %>% 
  mutate(Sexo = ifelse(Sexo %in% c('No Definido', 'No Reportado'), "No definido/No reportado", Sexo)) %>% 
  group_by(Sexo, TipoAlteracion) %>% 
  summarise(n = sum(n))

ggplot(data=discapac, aes(x=fct_reorder(stringr::str_wrap(TipoAlteracion, 30), n), y=n, fill=Sexo)) +
  geom_bar(stat="identity", position=position_dodge())+
  geom_text(aes(label = format(n, big.mark = ".", scientific = FALSE)), vjust=0.4, 
            position = position_dodge(0.9), size=3.5)+
  scale_fill_brewer(palette="Pastel1")+
  xlab("") + ylab("") + 
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90))+
  coord_flip() 
 
#ggsave("./graphs/Etnia.png", scale = 1.6, width = 4, height = 2.2)


# Personas UARIV
inputShapes <- file.path("../input/ShapeFiles")
shapColDep <- st_read(file.path(inputShapes, "depto","depto.shp"))
    
nombresDep <- as.data.frame(shapColDep) %>% 
      select(DPTO, NOMBRE_DPT) %>% 
      distinct()
    
    numeroVictimasDep <- RUVCom1 %>% 
      group_by(DepartamentoResidencia) %>% 
      summarise(nRes = n()) %>% 
      mutate(DepartamentoResidencia = stringr::str_trim(DepartamentoResidencia, "both")) %>% 
      mutate(DepartamentoResidencia = toupper(DepartamentoResidencia)) %>% 
      dplyr::filter(DepartamentoResidencia != "1") %>% 
      mutate(porcRes = (nRes/sum(nRes))*100) %>% 
      dplyr::rename(NOMBRE_DPT = DepartamentoResidencia) %>% 
      mutate(NOMBRE_DPT = ifelse(NOMBRE_DPT == "ARCHIPI??LAGO DE SAN ANDR??RS, PROVIDENCIA Y SANTA CATALINA", "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA", 
                                 ifelse(NOMBRE_DPT == "ATL??NTICO", "ATLANTICO",
                                        ifelse(NOMBRE_DPT == "BOL??VAR", "BOLIVAR",
                                               ifelse(NOMBRE_DPT == "BOYAC??", "BOYACA",
                                                      ifelse(NOMBRE_DPT == "CAQUET??", "CAQUETA",
                                                             ifelse(NOMBRE_DPT == "CHOC??", "CHOCO",
                                                                    ifelse(NOMBRE_DPT == "C??RDOBA", "CORDOBA",
                                                                           ifelse(NOMBRE_DPT == "GUAIN??A", "GUAINIA",
                                                                                  ifelse(NOMBRE_DPT == "BOGOT??, D.C.", "SANTAFE DE BOGOTA D.C",
                                                                                         ifelse(NOMBRE_DPT == "VAUP??S", "VAUPES",NOMBRE_DPT))))))))))) %>% 
      left_join(nombresDep) 
    
    numeroVictimasDepOcur <- RUVCom1 %>% 
      group_by(DepartamentoOcurrencia) %>% 
      summarise(nOcu = n()) %>% 
      mutate(DepartamentoOcurrencia = stringr::str_trim(DepartamentoOcurrencia, "both")) %>% 
      mutate(DepartamentoOcurrencia = toupper(DepartamentoOcurrencia)) %>% 
      dplyr::filter(DepartamentoOcurrencia != "1") %>% 
      mutate(porcOcur = (nOcu/sum(nOcu))*100) %>% 
      dplyr::rename(NOMBRE_DPT = DepartamentoOcurrencia) %>% 
      mutate(NOMBRE_DPT = ifelse(NOMBRE_DPT == "ARCHIPI??LAGO DE SAN ANDR??S, PROVIDENCIA Y SANTA CATALINA", "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA", 
                                 ifelse(NOMBRE_DPT == "ATL??NTICO", "ATLANTICO",
                                        ifelse(NOMBRE_DPT == "BOL??VAR", "BOLIVAR",
                                               ifelse(NOMBRE_DPT == "BOYAC??", "BOYACA",
                                                      ifelse(NOMBRE_DPT == "CAQUET??", "CAQUETA",
                                                             ifelse(NOMBRE_DPT == "CHOC??", "CHOCO",
                                                                    ifelse(NOMBRE_DPT == "C??RDOBA", "CORDOBA",
                                                                           ifelse(NOMBRE_DPT == "GUAIN??A", "GUAINIA",
                                                                                  ifelse(NOMBRE_DPT == "BOGOT??, D.C.", "SANTAFE DE BOGOTA D.C",
                                                                                         ifelse(NOMBRE_DPT == "VAUP??S", "VAUPES",NOMBRE_DPT))))))))))) %>% 
      left_join(nombresDep) 

    conteos = numeroVictimasDep %>% 
      left_join(numeroVictimasDepOcur)
    
    BDMapa <- shapColDep %>% 
      left_join(conteos) %>% 
      mutate(porcRes = round(porcRes, 2), porcOcur = round(porcOcur, 2)) 
    
    # Mapa de % atencion victimas
    tm_shape(BDMapa) + 
      tm_polygons("porcOcur", id = "NOMBRE_DPT", palette = "PuBu",
                  title = "% ",
                  textNA = "")
    mapaVict <- tmap_last()
    tmap_save(mapaVict, "mapaResidencia.html")
    
       # carga la muestra
    
    load("../input/RIPSImpacto.rdata")
    
    write.table(RIPS, "../RIPS.txt", sep = ";")
    
    correlationsDB = RIPS %>% 
      select(PersonaID:Sexo, FinalidadConsulta:CausaExterna, Procedimiento:MpioAtencion) %>% 
      select(-Procedimiento, -DiagnosticoPrincipal, -Sexo) %>% 
      distinct() %>% 
      left_join(RUVCom1) %>% 
      select(-contains("CodMun"), -contains("CodDep"), -Administradora, -contains("unicipio"), -Edad, -contains("Departamento"), -contains("Fecha"), -MpioAtencion) %>% 
      mutate(EdadAtencion = ifelse(EdadAtencion >= 100, 100, EdadAtencion)) %>% 
      mutate(GrupoEdadAtencion = cut(EdadAtencion,breaks = seq(0, 100, by = 10),  include.lowest = TRUE))  %>% 
      select(-quinquenio, -GrupoEdad)

    
    correlationsDBDummy3 <-correlationsDB %>% 
      select(-MuncipioResidencia, -EdadAtencion, -MuncipioResidencia, -MuncipioOcurrencia) %>% 
      distinct()
    
    correlationsDBDummyA <- correlationsDBDummy3 %>% 
      select(PersonaID)
    correlationsDBDummy3 <- fastDummies::dummy_cols(correlationsDBDummy3, ignore_na = TRUE)
    
    correlationsDBDummy3 <- correlationsDBDummy3 %>% 
      select(-(TipoAtencion:GrupoEdadAtencion))
    
    rm(correlationsDB, correlationsDBDummy3, correlationsDBDummyA, RIPS, RUVCom1)
    
    
    save(correlationsDBDummyFinal, file = "~/Desktop/DS4A/FinalProject/files/BDCor.rdata")
    correlationsDBDummyFinal <-correlationsDBDummyA %>% 
      bind_cols(correlationsDBDummy3) 
    
asociaciones <- NULL
    
    for(i in c(3:ncol(correlationsDBDummyFinal))) {
      print(i)
      for(j in c(3:ncol(correlationsDBDummyFinal))){
        
        if(!(i <= j)){
          a = as.matrix(table(correlationsDBDummyFinal[,c(i, j)]))
          
          ind = assocstats(a)
          
          vect <- c(colnames(correlationsDBDummyFinal[,i]), colnames(correlationsDBDummyFinal[,j]), ind$phi, ind$contingency, ind$cramer) %>% 
            t() %>% 
            as.data.frame()
          
          asociaciones <- asociaciones %>% 
            bind_rows(vect)
        }

      }
    }
save(asociaciones, file = "~/Desktop/DS4A/FinalProject/files/Asociaciones.rdata")

asociaciones <- asociaciones %>% 
  mutate(Phi = as.numeric(Phi), Contigencia = as.numeric(Contigencia), Cramer = as.numeric(Cramer))
colnames(asociaciones) <- c("Var1", "Var2", "Phi", "Contigencia", "Cramer")

write.xlsx(asociaciones, file.path(output, "asociaciones.xlsx"))


# Procesamiento



#  mapas  ---------------- 

boletin = read.xlsx(file.path('~/Desktop/Corte/input', "Boletin.xlsx"), sheet = "mapa")
mapas = RUV %>% 
  group_by(CodDepOcur, DepartamentoOcurrencia) %>% 
  summarise(nVictimas = sum(n)) %>% 
  ungroup() %>% 
  mutate(CodDepOcur = str_pad(CodDepOcur, 2, pad = "0"))

mapas = mapas %>% 
  dplyr::rename(DPTO = CodDepOcur) %>% 
  inner_join(boletin) %>% 
  mutate(Victims1000 = round(nVictimas*1000/Poblaci??n, 2))

inputShapes <- file.path("~/Desktop/Corte/input/ShapeFiles")
shapColDep <- st_read(file.path(inputShapes, "depto","depto.shp"))

BDMapa <- shapColDep %>% 
  left_join(mapas) 


tm_shape(BDMapa) + 
  tm_polygons("Victims1000")

tm_shape(BDMapa) + 
  tm_polygons("Victims1000", id = "DepartamentoOcurrencia", palette = "YlGnBu",
              title = "No. victims per 1000 hab.",
              textNA = "") +
  tm_shape(BDMapa) + 
  tm_bubbles(size = "nVictimas", palette="-RdYlBu", contrast=1, 
             title.size="Number of victims", col = "red", 
             breaks = c(0,500000, 1000000, 1500000, 2000000),
             labels = c("0.5 mill", "1 mill", "1.5 mill", '2 mill')) +
  tm_text("DepartamentoOcurrencia", size = 0.7, shadow=TRUE) + 
  tm_borders(lwd=2) +
  tm_layout(legend.outside = FALSE)

# Loading RIPS -----------------------

RIPS = read.table(file = "./files/AgregaRIPSConteo.txt", sep = "|")

RIPS1 = RIPS %>% 
  filter(n<=100)

depaRIPS = RIPS1 %>% 
  group_by(PersonaID, anoAtencion, CodDptoAtencion, DepartamentoAtencion) %>% 
  summarise(total = sum(n)) %>% 
  group_by(CodDptoAtencion, DepartamentoAtencion, anoAtencion) %>%
  summarise(atencionPromedio= mean(total, na.rm = TRUE)) %>% 
  group_by(CodDptoAtencion, DepartamentoAtencion) %>% 
  summarise(atencionPromedio= mean(atencionPromedio, na.rm = TRUE)) %>% 
  left_join(RIPS1 %>% 
              group_by(CodDptoAtencion) %>% 
              summarise(numeroAtencionAno = sum(n)/6))

depaRIPS = depaRIPS %>% 
  ungroup() %>% 
  mutate(CodDptoAtencion = str_pad(CodDptoAtencion, 2, pad = "0")) %>% 
  dplyr::rename(DPTO = CodDptoAtencion) 

BDMapa1 <- shapColDep %>% 
  left_join(depaRIPS) 

tm_shape(BDMapa1) + 
  tm_polygons("atencionPromedio", id = "DepartamentoAtencion", palette = "PuBuGn",
              title = "Average health service use",
              textNA = "") +
  tm_shape(BDMapa1) + 
  tm_bubbles(size = "numeroAtencionAno", col = 'darkslateblue',  
             title.size="Number of health services") +
  tm_text("DepartamentoAtencion", size = 0.7) + 
  tm_borders(lwd=2) +
  tm_layout(legend.outside = FALSE)

EtniaRIPS = RIPS1 %>% 
  mutate(Etnia = as.character(Etnia)) %>% 
  mutate(Etnia = ifelse(is.na(Etnia), "Ninguna", Etnia)) %>% 
  group_by(PersonaID, anoAtencion, Etnia) %>% 
  summarise(total = sum(n)) %>% 
  group_by(Etnia, anoAtencion) %>%
  summarise(atencionPromedio= mean(total, na.rm = TRUE),Error = sd(total, na.rm = TRUE)/sqrt(n())) %>% 
  mutate(label = round(atencionPromedio, 1))

pd <- position_dodge(0.1)


ggplot(EtniaRIPS, aes(x=anoAtencion, y=atencionPromedio, colour=Etnia)) + 
  geom_errorbar(aes(ymin=atencionPromedio-Error, ymax=atencionPromedio+Error), width=.1, position=pd) +
  geom_line(position=pd) +
  geom_label_repel(aes(label = label),
                   box.padding   = 0.35, 
                   point.padding = 0.5,
                   segment.color = 'grey50') +
  #geom_text(aes(label=label),hjust=0, vjust=0, color = 'black')+
  geom_point(position=pd,shape=21, fill="white") + 
  scale_color_brewer(palette="Paired") +
  xlab("Year") + 
  ylab("Average health service use") + 
  theme_bw()

ciclovidaRIPS = RIPS1 %>% 
  filter(!is.na(GrupoEdad)) %>% 
  mutate(Ciclovida = ifelse(GrupoEdad %in% c('[0,5)', '[5,10)'), 'Early childhood and infancy',
                                   ifelse(GrupoEdad %in% c('[10,15)','[15,20)', '[20,25)'), "Adolescence and youth", 
                                          ifelse(GrupoEdad %in% c('[25,30)',  '[30,35)',  '[35,40)', '[40,45)', '[45,50)',  '[50,55)', '[55,60)', '[60,65)'), 'Adulthood','Elderly')))) %>% 
  group_by(PersonaID, anoAtencion, Ciclovida) %>% 
  summarise(total = sum(n)) %>% 
  group_by(Ciclovida, anoAtencion) %>%
  summarise(atencionPromedio= mean(total, na.rm = TRUE),Error = sd(total, na.rm = TRUE)/sqrt(n())) %>% 
  mutate(label = round(atencionPromedio, 1))

ggplot(ciclovidaRIPS, aes(x=anoAtencion, y=atencionPromedio, colour=Ciclovida)) + 
  geom_errorbar(aes(ymin=atencionPromedio-Error, ymax=atencionPromedio+Error), colour="black", width=.1, position=pd) +
  geom_line(position=pd) +
  geom_label_repel(aes(label = label),
                   box.padding   = 0.35, 
                   point.padding = 0.5,
                   segment.color = 'grey50') +
  #geom_text(aes(label=label),hjust=0, vjust=0, color = 'black')+
  geom_point(position=pd,shape=21, fill="white") + 
  scale_color_brewer(palette="Paired") +
  xlab("Year") + 
  ylab("Average health service use") + 
  theme(legend.title = element_blank()) +theme_bw() +
  theme(legend.title = element_blank())

sexoRIPS = RIPS1 %>%   mutate(Sexo = as.character(Sexo)) %>% 
  mutate(Sexo = ifelse(Sexo %in% c('No Definido', 'No Reportado'), "No definido/No reportado", Sexo)) %>% 
  group_by(PersonaID, anoAtencion, Sexo) %>% 
  summarise(total = sum(n)) %>% 
  group_by(Sexo, anoAtencion) %>%
  summarise(atencionPromedio= mean(total, na.rm = TRUE),Error = sd(total, na.rm = TRUE)/sqrt(n())) %>% 
  mutate(label = round(atencionPromedio, 1))

ggplot(sexoRIPS, aes(x=anoAtencion, y=atencionPromedio, colour=Sexo)) + 
  geom_errorbar(aes(ymin=atencionPromedio-Error, ymax=atencionPromedio+Error), colour="black", width=.1, position=pd) +
  geom_line(position=pd) +
  geom_label_repel(aes(label = label),
                   box.padding   = 0.35, 
                   point.padding = 0.5,
                   segment.color = 'grey50') +
  #geom_text(aes(label=label),hjust=0, vjust=0, color = 'black')+
  geom_point(position=pd,shape=21, fill="white") + 
  scale_color_brewer(palette="Paired") +
  xlab("Year") + 
  ylab("Average health service use") + 
  theme(legend.title = element_blank()) +theme_bw() +
  theme(legend.title = element_blank())

discapaciRIPS = RIPS1 %>% 
  dplyr::rename(Disability = IndDiscapacidad) %>%
  group_by(PersonaID, anoAtencion, Disability) %>% 
  summarise(total = sum(n)) %>% 
  group_by(Disability, anoAtencion) %>%
  summarise(atencionPromedio= mean(total, na.rm = TRUE),Error = sd(total, na.rm = TRUE)/sqrt(n())) %>% 
  mutate(label = round(atencionPromedio, 1))

ggplot(discapaciRIPS, aes(x=anoAtencion, y=atencionPromedio, colour=Disability)) + 
  geom_errorbar(aes(ymin=atencionPromedio-Error, ymax=atencionPromedio+Error), colour="black", width=.1, position=pd) +
  geom_line(position=pd) +
  geom_label_repel(aes(label = label),
                   box.padding   = 0.35, 
                   point.padding = 0.5,
                   segment.color = 'grey50') +
  #geom_text(aes(label=label),hjust=0, vjust=0, color = 'black')+
  geom_point(position=pd,shape=21, fill="white") + 
  scale_color_brewer(palette="Paired") +
  xlab("Year") + 
  ylab("Average health service use") + 
  theme(legend.title = element_blank()) +theme_bw() +
  theme(legend.title = element_blank())

enfermedadesRIPS = modelos %>% 
  select(PersonaID:Tumor, Total) %>% 
  gather(Patologia, Valor, -PersonaID, -Total) %>% 
  #filter(Valor == 1) %>% 
  group_by(Patologia, Valor) %>% 
  summarise(atencionPromedio = mean(Total, na.rm = TRUE), Error = sd(Total, na.rm = TRUE)/sqrt(n()))  %>% 
  mutate(label = round(atencionPromedio, 1)) %>% 
  ungroup() %>% 
  mutate(Patologia = ifelse(Patologia == 'Cerebro', 'Cerebrovascular', 
                            ifelse(Patologia == 'Hipertension', 'Hypertension',
                                   ifelse(Patologia == 'Infarto','Heart attack', Patologia)))) %>% 
  mutate(Valor = ifelse(Valor == 0, "No", "Si"))

ggplot(enfermedadesRIPS, aes(x=fct_reorder(Patologia, -atencionPromedio), y=atencionPromedio, fill=Valor)) + 
  geom_bar(position=position_dodge(), stat="identity") +
  geom_errorbar(aes(ymin=atencionPromedio-Error, ymax=atencionPromedio+Error),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9)) +
  scale_fill_brewer(palette="Paired") +
  xlab("Year") + 
  ylab("Average health service use") + 
  theme(legend.title = element_blank()) +theme_bw() +
  theme(legend.title = element_blank())




# Graphics Time Line

agregaMes = read.table(file = "./files/agregaRIPSMesAno.txt",sep = "|")

agregaMes <- agregaMes %>% 
  filter(!is.na(TipoAtencion)) %>% 
  mutate(mesAtencion = str_pad(mesAtencion, 2, pad = "0")) %>% 
  mutate(mesAno = paste(anoAtencion, mesAtencion, sep = "-")) %>% 
  mutate(mesAno = as.Date(mesAno,format='%Y-%m'))

month <- "2009-03"
as.Date(paste(month,"-01",sep=""))
ggplot(agregaMes, aes(x = mesAno, y = n)) + 
  geom_area(aes(color = TipoAtencion, fill = TipoAtencion), 
            alpha = 0.5, position = position_dodge(0.8))

