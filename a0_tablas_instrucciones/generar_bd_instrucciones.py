#!/usr/bin/python3

from dataclasses import dataclass
from typing import List
from utilidades.documentos.Documento import Documento

import sqlite3

class Flag(object):
    def __init__(self, nombre, valor) -> None:
        self.nombre=nombre
        self.valor=valor
    def __str__(self) -> str:
        formato="{0}:{1}"
        return formato.format(self.nombre, self.valor)
    
CAMPO_MNEMONICO="MNEMONICO"
CAMPO_CICLOS="CICLOS"
CAMPO_TAM="TAMANO"
CAMPO_FLAG_S="FLAG_S"
CAMPO_FLAG_Z="FLAG_Z"
CAMPO_FLAG_H="FLAG_H"
CAMPO_FLAG_P="FLAG_P"
CAMPO_FLAG_N="FLAG_N"
CAMPO_FLAG_C="FLAG_C"
CAMPO_CODOP="CODOP"
CAMPO_DESCRIPCION="DESCRIPCION"
CAMPO_NOTAS="NOTAS"
NOMBRE_TABLA_INSTRUCCIONES="INSTRUCCIONES"
SQL_CREAR_TABLA_INSTRUCCIONES="""
create table {0} 
(
    {1} CHAR(16),
    {2} INT,
    {3} INT,
    {4} CHAR(1),
    {5} CHAR(1),
    {6} CHAR(1),
    {7} CHAR(1),
    {8} CHAR(1),
    {9} CHAR(1),
    {10} CHAR(16),
    {11} CHAR(16),
    {12} CHAR(16)
    
);
""".format(NOMBRE_TABLA_INSTRUCCIONES, CAMPO_MNEMONICO, CAMPO_CICLOS, CAMPO_TAM,
CAMPO_FLAG_S, CAMPO_FLAG_Z, CAMPO_FLAG_H, CAMPO_FLAG_P, CAMPO_FLAG_N, CAMPO_FLAG_C,
CAMPO_CODOP, CAMPO_DESCRIPCION, CAMPO_NOTAS)

SQL_INSERT="""
INSERT INTO {0}
(
 '{1}' , '{2}' , '{3}' , '{4}' , '{5}' , '{6}' , '{7}' , '{8}' , '{9}', '{10}', '{11}', '{12}'
    
) VALUES 
""".format(NOMBRE_TABLA_INSTRUCCIONES, CAMPO_MNEMONICO, CAMPO_CICLOS, CAMPO_TAM,
CAMPO_FLAG_S, CAMPO_FLAG_Z, CAMPO_FLAG_H, CAMPO_FLAG_P, CAMPO_FLAG_N, CAMPO_FLAG_C,
CAMPO_CODOP, CAMPO_DESCRIPCION, CAMPO_NOTAS)


@dataclass
class Instruccion(object):
    mnemonico:str
    ciclos_reloj:str
    condicional:bool
    ciclos_reloj_si_condicion_se_cumple:int
    ciclos_reloj_si_condicion_no_se_cumple:int
    bytes:int
    flags:List[Flag]
    opcode:str
    descripcion:str
    notas:str

    def __init__(self) -> None:
        self.ciclos_reloj=0
        self.ciclos_reloj_si_condicion_no_se_cumple=0
        self.ciclos_reloj_si_condicion_se_cumple=0 
        self.flags=[]
    
    def set_mnemonico(self, trozos):
        campo = trozos[1].strip()
        
        self.mnemonico=campo
    
        
    def set_ciclos(self, trozos):
        campo=trozos[2]
        #print(campo)
        if campo.find("/")==-1:
            self.condicional=False
            self.ciclos_reloj=int(campo.strip())
            self.ciclos_reloj_si_condicion_no_se_cumple=0
            self.ciclos_reloj_si_condicion_se_cumple=0 
        else:
            #Sí es condicional
            self.condicional=True
            ciclos=campo.split("/")
            self.ciclos_reloj_si_condicion_se_cumple=int(ciclos[0])
            self.ciclos_reloj_si_condicion_no_se_cumple=int(ciclos[1])
    
    def set_bytes(self, trozos):
        campo=trozos[3]
        self.bytes=int(campo)

    def set_flags(self, trozos):
        campo=trozos[4]
        flags=["S", "Z", "H", "P", "N", "C"]
        lista_flags=[]
        for pos, valor in enumerate(campo):
            flag=Flag(flags[pos], campo[pos])
            lista_flags.append(flag)
        self.flags=lista_flags

    def set_opcode(self, trozos):
        self.opcode=trozos[5].strip()

    def set_descripcion(self, trozos):
        self.descripcion=trozos[6].strip()

    def set_notas(self, trozos):
        self.notas=trozos[7].strip()

    def build(self, trozos):
        self.set_mnemonico(trozos)
        self.set_ciclos(trozos)
        self.set_bytes(trozos)
        self.set_flags(trozos)
        self.set_opcode(trozos)
        self.set_descripcion(trozos)
        self.set_notas(trozos)
    
    def modificar_asterisco(self, flag):
        if flag=="*":
            return "x"
        else:
            return flag

    def get_flags(self):
        flags="".join([self.modificar_asterisco( self.flags[0].valor ), 
            self.modificar_asterisco( self.flags[1].valor ), 
            self.modificar_asterisco( self.flags[2].valor ), 
            self.modificar_asterisco( self.flags[3].valor ), 
            self.modificar_asterisco( self.flags[4].valor ), 
            self.modificar_asterisco( self.flags[5].valor )])
        return flags

    def get_valores(self):
        lista=[
            self.mnemonico, self.get_ciclos_reloj(), self.bytes,
            " "+self.get_flags()+" ",
            self.opcode, self.descripcion, self.notas
        ]
        return lista

    def get_ciclos_reloj(self):
        if self.condicional:
            return "{0}/{1}".format(self.ciclos_reloj_si_condicion_se_cumple, self.ciclos_reloj_si_condicion_no_se_cumple)
        return self.ciclos_reloj

    def get_sql_insert(self):
        valores="""
        ("{0}", {1}, {2}, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', "{11}")
        """
        insert=valores.format(self.mnemonico, self.get_ciclos_reloj(), self.bytes,
        self.flags[0].valor, self.flags[1].valor, self.flags[2].valor,
        self.flags[3].valor, self.flags[4].valor, self.flags[5].valor,
        self.opcode, self.descripcion, self.notas)
        return SQL_INSERT+ insert

def generar_documento_instrucciones(self, lista_instrucciones):
        #Generamos la tabla de instrucciones en formato RST
        documento_instrucciones=Documento("Instrucciones.rst")
        
        filas=[]
        for i in lista_instrucciones:
            filas.append(i.get_valores())
        
        cabeceras=["Mnemónico", "Ciclos", "Bytes", "SZHPNC", "COD OP","Descr.", "Notas"]
        documento_instrucciones.anadir_tabla("Instrucciones.rst", 
        cabeceras, filas)
        documento_instrucciones.guardar()
        print("RST Generado")

def extraer_informacion_instrucciones_en_sqlite(nombre_archivo_instrucciones, nombre_bd_sqlite):
    instrucciones=[]
    with open (nombre_archivo_instrucciones, "r") as fich:
        lineas=fich.readlines()

        for l in lineas[1:]:
            trozos=l.strip().split("|")
            instruccion=Instruccion()
            instruccion.build(trozos)
            instrucciones.append(instruccion)
            #print(trozos)
        #Fin del for
        #Creamos la BD
        conexion=sqlite3.connect("instrucciones.db")
        cursor=conexion.cursor()
        sql_crear_tabla=SQL_CREAR_TABLA_INSTRUCCIONES
        #print(sql_crear_tabla)
        cursor.execute(sql_crear_tabla)
        for i in instrucciones:
            #print(i.get_sql_insert())
            #print(SQL_CREAR_TABLA_INSTRUCCIONES)
            cursor.execute(i.get_sql_insert())
        conexion.commit()
        #generar_documento_instrucciones("Instrucciones.rst", instrucciones)

if __name__=="__main__":
    extraer_informacion_instrucciones_en_sqlite("tabla_instrucciones.txt", "instrucciones.db")
    