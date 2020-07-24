http://192.168.50.165:8888/?token=dc308c99ccd22647ba67cfbf0031af9531e2c574e4be1e45



drop table TB_RUV;

/*==============================================================*/
/* Table: TB_RUV                                                */
/*==============================================================*/
create table TB_RUV (
   PERSONAID            VARCHAR(16)          not null,
   SEXO                 VARCHAR(16)          null,
   ETNIA                VARCHAR(32)          null,
   INDDISCAPACIDAD      VARCHAR(2)           null,
   FECHANACIMIENTO      DATE                 null,
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
   ZONAOCURRENCIA       VARCHAR(128)         null,
   constraint PK_TB_RUV primary key (PERSONAID)
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

drop table TB_RIPS;

/*==============================================================*/
/* Table: TB_RIPS                                               */
/*==============================================================*/
create table TB_RIPS (
   PERSONAID            VARCHAR(16)          null,
   TIPOATENCION         VARCHAR(128)         null,
   CAPITULODX           VARCHAR(128)         null,
   DIAGNOSTICOPRINCIPAL VARCHAR(255)         null,
   EDADATENCION         VARCHAR(16)         null,
   SEXO                 VARCHAR(16)          null,
   FECHAATENCION        DATE                null,
   FECHAATENCION_str    VARCHAR(128)                 null,
   FINALIDADCONSULTA    VARCHAR(128)         null,
   FINALIDADPROCEDIMIENTO VARCHAR(128)         null,
   CAUSAEXTERNA         VARCHAR(128)         null,
   CODIGOPRESTADOR      VARCHAR(128)         null,
   PRESTADOR            VARCHAR(128)         null,
   PROCEDIMIENTO        VARCHAR(512)         null,
   DPTOIDATENCION       VARCHAR(128)         null,
   DPTOATENCION         VARCHAR(128)         null,
   MPIOIDATENCION       VARCHAR(128)         null,
   MPIOATENCION         VARCHAR(128)         null,
   NUMEROATENCIONES     VARCHAR(16)                null
);

comment on table TB_RIPS is
'Contiene información sobre la atención médica realizada';

alter table TB_RIPS
   add constraint FK_TB_RIPS_REFERENCE_TB_RUV foreign key (PERSONAID)
      references TB_RUV (PERSONAID)
      on delete restrict on update restrict;


CREATE INDEX tb_rips_sexo ON tb_rips (sexo);
CREATE INDEX tb_rips_dptoatencion ON tb_rips (dptoatencion);