create database ds4a_team61;

create user team61_user with encrypted password 'ds4at34m61';

grant all privileges on database ds4a_team61 to team61_user;


drop table TB_RUV;

/*==============================================================*/
/* Table: TB_RUV                                                */
/*==============================================================*/
create table TB_RUV (
   PERSONAID            VARCHAR(16)          not null,
   SEXO                 VARCHAR(32)          null,
   ETNIA                VARCHAR(128)          null,
   INDDISCAPACIDAD      VARCHAR(2)           null,
   FECHANACIMIENTO      DATE                 null,
   FECHANACIMIENTO_STR  VARCHAR(128)                 null,
   HECHO                VARCHAR(128)         null,
   DEPARTAMENTOIDRESIDENCIA VARCHAR(128)         null,
   DEPARTAMENTORESIDENCIA VARCHAR(128)         null,
   MUNCIPIOIDRESIDENCIA VARCHAR(128)         null,
   MUNCIPIORESIDENCIA   VARCHAR(128)         null,
   DEPARTAMENTOIDOCURRENCIA VARCHAR(128)         null,
   DEPARTAMENTOOCURRENCIA VARCHAR(128)         null,
   MUNCIPIOIDOCURRENCIA VARCHAR(128)         null,
   MUNCIPIOOCURRENCIA   VARCHAR(128)         null,
   SUJETODESC           VARCHAR(128)         null,
   ZONAOCURRENCIA       VARCHAR(128)         null
);

comment on table TB_RUV is
'Contiene información sobre víctimas registradas, datos de ubicación de la víctima, categoría del acto de victimización, entre otros.';

alter table TB_RUV
   add constraint FK_TB_RUV_REFERENCE_TB_MUNIC foreign key (MUNCIPIORESIDENCIA)
      references TB_MUNICIPIOS (MUNICIPIOID)
      on delete restrict on update restrict;

alter table TB_RUV
   add constraint FK_TB_RUV_REFERENCE_TB_MUNIC foreign key (MUNCIPIOOCURRENCIA)
      references TB_MUNICIPIOS (MUNICIPIOID)
      on delete restrict on update restrict;
	  
	  

drop table TB_RUAF;

/*==============================================================*/
/* Table: TB_RUAF                                               */
/*==============================================================*/
create table TB_RUAF (
   PERSONABASICAID      VARCHAR(16)          not null,
   TIPOREGIMEN          VARCHAR(128)         null,
   ESTADOAFILIACION     VARCHAR(128)         null,
   ADMINISTRADORA       VARCHAR(128)         null,
   TIPOAFILIADO         VARCHAR(128)         null,
   DEPARTAMENTOIDAFILIACION VARCHAR(128)         null,
   DEPARTAMENTOAFILIACION VARCHAR(128)         null,
   MUNICIPIOIDAFILIACION VARCHAR(128)         null,
   MUNICIPIOAFILIACION  VARCHAR(128)         null,
   FECHAAFILIACION      DATE                 null,
   AREA                 VARCHAR(128)         null,
   constraint PK_TB_RUAF primary key (PERSONABASICAID)
);

comment on table TB_RUAF is
'Proporciona información sobre el estado de la afiliación de las personas al Sistema de Seguridad Social';

alter table TB_RUAF
   add constraint FK_TB_RUAF_REFERENCE_TB_RUV foreign key (PERSONABASICAID)
      references TB_RUV (PERSONAID)
      on delete restrict on update restrict;
	  
	  
	  
drop table TB_RLCPD;

/*==============================================================*/
/* Table: TB_RLCPD                                              */
/*==============================================================*/
create table TB_RLCPD (
   PERSONAID            VARCHAR(16)          not null,
   FECHAREGISTRO        DATE                 null,
   TIPOALTERACION       VARCHAR(128)         null,
   ORIGENDISCAPACIDAD   VARCHAR(128)         null,
   DEPARTAMIENTOIDREGISTRO VARCHAR(128)         null,
   DEPARTAMIENTOREGISTRO VARCHAR(128)         null,
   MINUCIPIOIDREGISTRO  VARCHAR(128)         null,
   MINUCIPIOREGISTRO    VARCHAR(128)         null,
   constraint PK_TB_RLCPD primary key (PERSONAID)
);

comment on table TB_RLCPD is
'Contiene los datos de caracterización de personas con discapacidad';

alter table TB_RLCPD
   add constraint FK_TB_RLCPD_REFERENCE_TB_RUV foreign key (PERSONAID)
      references TB_RUV (PERSONAID)
      on delete restrict on update restrict;


drop table TB_DEFUNCIONES;

/*==============================================================*/
/* Table: TB_DEFUNCIONES                                        */
/*==============================================================*/
create table TB_DEFUNCIONES (
   PERSONAID            VARCHAR(16)          not null,
   FECHADEFUNCION       DATE                 null,
   PROBABLEMANERAMUERTE VARCHAR(128)         null,
   PROBABLEMANERAMUERTEVIOLENTA VARCHAR(128)         null,
   constraint PK_TB_DEFUNCIONES primary key (PERSONAID)
);

comment on table TB_DEFUNCIONES is
'Contiene los datos de defunciones';

alter table TB_DEFUNCIONES
   add constraint FK_TB_DEFUN_REFERENCE_TB_RUV foreign key (PERSONAID)
      references TB_RUV (PERSONAID)
      on delete restrict on update restrict;


drop table TB_RIPS;

/*==============================================================*/
/* Table: TB_RIPS                                               */
/*==============================================================*/
create table TB_RIPS (
   PERSONAID              VARCHAR(16)          null,
   TIPOATENCION           VARCHAR(128)         null,
   CAPITULODX             VARCHAR(128)         null,
   DIAGNOSTICOPRINCIPAL   VARCHAR(255)         null,
   EDADATENCION           VARCHAR(16)          null,
   SEXO                   VARCHAR(16)          null,
   FECHAATENCION          DATE                 null,
   FECHAATENCION_STR      VARCHAR(128)         null,
   FINALIDADCONSULTA      VARCHAR(128)         null,
   FINALIDADPROCEDIMIENTO VARCHAR(128)         null,
   CAUSAEXTERNA           VARCHAR(128)         null,
   CODIGOPRESTADOR        VARCHAR(128)         null,
   PRESTADOR              VARCHAR(128)         null,
   PROCEDIMIENTO          VARCHAR(512)         null,
   DPTOIDATENCION         VARCHAR(128)         null,
   DPTOATENCION           VARCHAR(128)         null,
   MPIOIDATENCION         VARCHAR(128)         null,
   MPIOATENCION           VARCHAR(128)         null,
   NUMEROATENCIONES       VARCHAR(16)          null
);

comment on table TB_RIPS is
'Contiene información sobre la atención médica realizada';

alter table TB_RIPS
   add constraint FK_TB_RIPS_REFERENCE_TB_RUV foreign key (PERSONAID)
      references TB_RUV (PERSONAID)
      on delete restrict on update restrict;

CREATE INDEX tb_rips_sexo ON tb_rips (sexo);
CREATE INDEX tb_rips_dptoatencion ON tb_rips (dptoatencion);


/* ------------------------- TABLAS MODELOS --------------------------------- */

drop table if exists tb_modelos;


/*==============================================================*/
/* Table: tb_modelos                                            */
/*==============================================================*/
CREATE TABLE tb_modelos (
  Ind BIGINT,
  PersonaID BIGINT,
  Cerebro BIGINT,
  Diabetes BIGINT,
  Hipertension BIGINT,
  Infarto BIGINT,
  Mental BIGINT,
  Tumor BIGINT,
  Sexo VARCHAR(128),
  Etnia VARCHAR(128),
  IndDiscapacidad VARCHAR(128),
  IndAdultoMayor VARCHAR(128),
  IndEtnia VARCHAR(128),
  FechaNacimiento DATE,
  Hecho VARCHAR(128),
  DepartamentoOcurrencia VARCHAR(128),
  MuncipioOcurrencia VARCHAR(128),
  SujetoDesc VARCHAR(128),
  probableManeraMuerteviolenta VARCHAR(128),
  probableManeraMuerte VARCHAR(128),
  TipoAlteracion VARCHAR(128),
  OrigenDiscapacidad VARCHAR(128),
  TipoRegimen VARCHAR(32),
  Edad BIGINT,
  GrupoEdad VARCHAR(8),
  CicloVida VARCHAR(32),
  Total DOUBLE PRECISION,
  CONSULTAS DOUBLE PRECISION,
  HOSPITALIZACIONES DOUBLE PRECISION,
  PROCEDIMIENTOS_DE_SALUD DOUBLE PRECISION,
  URGENCIAS DOUBLE PRECISION,
  Region VARCHAR(32)
);

comment on table tb_ruv_agg is
'Contiene información requerida para la construcción de los modelos.';


/* ------------------------- TABLAS AGREGADAS --------------------------------- */

drop table if exists tb_ruv_agg;

/*==============================================================*/
/* Table: tb_ruv_agg                                            */
/*==============================================================*/
CREATE TABLE tb_ruv_agg (
  Ind BIGINT,
  IndDiscapacidad VARCHAR(128),
  IndAdultoMayor VARCHAR(128),
  IndEtnia VARCHAR(128),
  IndFallecido VARCHAR(128),
  IndVictima VARCHAR(128),
  Sexo VARCHAR(128),
  Etnia VARCHAR(128),
  Hecho VARCHAR(128),
  CodDepOcur varchar(16),
  DepartamentoOcurrencia VARCHAR(128),
  CodMunOcur varchar(16),
  MuncipioOcurrencia VARCHAR(128),
  SujetoDesc VARCHAR(128),
  ZonaOcurrencia VARCHAR(32),
  probableManeraMuerte VARCHAR(128),
  probableManeraMuerteviolenta VARCHAR(128),
  TipoAlteracion VARCHAR(128),
  OrigenDiscapacidad VARCHAR(128),
  TipoRegimen VARCHAR(32),
  EstadoAfiliacion VARCHAR(32),
  TipoAfiliado VARCHAR(24),
  GrupoEdad VARCHAR(8),
  IndMuestra VARCHAR(8),
  n BIGINT
);

comment on table tb_ruv_agg is
'Contiene información agregada sobre víctimas registradas, datos de ubicación de la víctima, categoría del acto de victimización, entre otros.';

create index tb_ruv_agg_sexo on tb_ruv_agg (sexo);

create index tb_ruv_agg_departamentoocurrencia on tb_ruv_agg (departamentoocurrencia)

create index tb_ruv_agg_coddepocur on tb_ruv_agg (coddepocur)

drop MATERIALIZED VIEW vm_ruv_agg;

create MATERIALIZED VIEW vm_ruv_agg
as
select trim(r.coddepocur) "CodigoDepartamento", trim(r.departamentoocurrencia) as "Departamento", r.indadultomayor as "EsAdultoMayor", r.indetnia as "PerteneceEtnia", r.etnia as "Etnia", r.inddiscapacidad as "TieneDiscapacidad", r.tipoalteracion as "Discapacidad", sum(n) as "Total"
from tb_ruv_agg r 
where coddepocur not in ('00','NA')
group by r.coddepocur, r.departamentoocurrencia, r.indadultomayor, r.indetnia, r.etnia, r.inddiscapacidad, r.tipoalteracion 
order by r.coddepocur, r.departamentoocurrencia, r.indadultomayor, r.indetnia, r.etnia, r.inddiscapacidad, r.tipoalteracion

drop table tb_rips_agg;

/*==============================================================*/
/* Table: tb_rips_agg                                           */
/*==============================================================*/
CREATE TABLE if exists tb_rips_agg (
  Ind BIGINT,
  PersonaID VARCHAR(128),
  TipoAtencion VARCHAR(128),
  CapituloDX VARCHAR(128),
  anoAtencion VARCHAR(4),
  n VARCHAR(16),
  IndDiscapacidad VARCHAR(128),
  IndAdultoMayor VARCHAR(128),
  IndEtnia VARCHAR(128),
  IndFallecido VARCHAR(128),
  IndVictima VARCHAR(128),
  Sexo VARCHAR(128),
  Etnia VARCHAR(128),
  Hecho VARCHAR(128),
  CodDepOcur varchar(16),
  DepartamentoOcurrencia VARCHAR(128),
  CodMunOcur varchar(16),
  MuncipioOcurrencia VARCHAR(128),
  SujetoDesc VARCHAR(128),
  ZonaOcurrencia VARCHAR(32),
  probableManeraMuerte VARCHAR(128),
  probableManeraMuerteviolenta VARCHAR(128),
  TipoAlteracion VARCHAR(128),
  OrigenDiscapacidad VARCHAR(128),
  TipoRegimen VARCHAR(32),
  EstadoAfiliacion VARCHAR(32),
  TipoAfiliado VARCHAR(24),
  GrupoEdad VARCHAR(8),
  IndMuestra varchar(8),
  CodDptoAtencion VARCHAR(16),
  DepartamentoAtencion VARCHAR(128),
  CodMunAtencion VARCHAR(16),
  MunicipioAtencion VARCHAR(128)
);

comment on table tb_rips_agg is
'Contiene información agregada sobre la atención médica realizada';


drop MATERIALIZED VIEW vm_rips_agg;

create MATERIALIZED VIEW vm_rips_agg
as
select trim(r.coddptoatencion) "CodigoDepartamento", trim(r.departamentoatencion) "Departamento", r.tipoatencion "TipoAtencion", r.capitulodx "CapituloDX", r.indadultomayor as "EsAdultoMayor", r.indetnia as "PerteneceEtnia", r.etnia as "Etnia", r.inddiscapacidad as "TieneDiscapacidad", r.tipoalteracion as "Discapacidad", sum(n::int) as "Total"
from tb_rips_agg r
where n <> 'NA'
and coddptoatencion not in ('00','NA')
group by r.coddptoatencion, r.departamentoatencion, r.tipoatencion, r.capitulodx, r.departamentoocurrencia, r.indadultomayor, r.indetnia, r.etnia, r.inddiscapacidad, r.tipoalteracion
order by r.coddptoatencion, r.departamentoatencion, r.tipoatencion, r.capitulodx, r.departamentoocurrencia, r.indadultomayor, r.indetnia, r.etnia, r.inddiscapacidad, r.tipoalteracion


drop table if exists tb_rips_agg_mesanno;

/*==============================================================*/
/* Table: tb_rips_agg_mesanno                                           */
/*==============================================================*/
CREATE TABLE tb_rips_agg_mesanno (
  TipoAtencion VARCHAR(128),
  anoAtencion VARCHAR(4),
  mesAtencion VARCHAR(2),
  CodDptoAtencion VARCHAR(16),
  DepartamentoAtencion VARCHAR(128),
  n BIGINT
);

comment on table tb_rips_agg is
'Contiene información agregada sobre la atención médica realizada agrupada por tipo atencion, ano, mes y departamento';