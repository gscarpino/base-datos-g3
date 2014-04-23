#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <set>

#define CANT_PROV 20
#define CANT_COMISIONES 45
#define CANT_PARTIDOS 6
#define CANT_DNI 10132
#define CANT_SENADORES CANT_PROV * 3
#define CANT_PROYECTOS 30

using namespace std;

string intToStr(int n){
     ostringstream ss;
     ss << n;
     return ss.str();
}

void insertarLegislador();
void insertarComisiones(unsigned int cant);
void insertarProvincias(unsigned int cant);
void insertarPartidoPolitico(unsigned int cant);
void insertarBloquePolitico(unsigned int cant);
void insertarCamaras();
void insertarBieneEconomico(unsigned int id, unsigned int valor, string tipo);
void insertarBienes();
void insertarPeriodo();
void insertarPartEnComisiones();
void insertarVice();
void insertarProyectos();
void insertarVoto();
void insertarEstudia();
void insertarPresideBloque();
void insertarSesiones();

bool dniValido(string dni);
string getDNI(string d);
string getNombre(string d);
string fechaAzar(unsigned int minAnio, unsigned int maxAnio);
unsigned int bloqueSenadoresAzar(unsigned int it, unsigned int cantBloques);
unsigned int bloqueDiputadosAzar(unsigned int it, unsigned int cantBloques);


set<string> conjDNI;
set<string> conjSen;
set<pair<string, string> > conjDipu;
unsigned int habitantes[CANT_PROV];

int main(){
    srand(time(NULL));
    insertarComisiones(CANT_COMISIONES);
    insertarProvincias(CANT_PROV);
    insertarPartidoPolitico(CANT_PARTIDOS);
    insertarBloquePolitico(CANT_PARTIDOS);
    insertarLegislador();
    insertarCamaras();
    insertarBienes();
    insertarPeriodo();
    insertarPartEnComisiones();
    insertarVice();
    insertarProyectos();
    insertarVoto();
    insertarEstudia();
    insertarPresideBloque();
    cout << "Termino" << endl;
    return 0;
}

void insertarComisiones(unsigned int cant){
    string query;
    for(unsigned int i = 0; i < cant; i++){
        query = string("insert into Comision (nombre_comision) values ('Comision") + intToStr(i+1) +  string("');");
        cout << query << endl;
    }
}


void insertarProvincias(unsigned int cant){
    string query;
    for(unsigned int i = 0; i < cant; i++){
        habitantes[i] = 100000 + (rand()*rand())%1000000;
        query = string("insert into Provincia (nombre,habitantes) values ('Provincia") + intToStr(i+1) +  string("',") + intToStr(habitantes[i]) + string(");");
        cout << query << endl;
    }
}


void insertarPartidoPolitico(unsigned int cant){
    string query;
    for(unsigned int i = 0; i < cant; i++){
        query = string("insert into Partido_politico (id_partido_politico,nombre) values (") + intToStr(i+1) +  string(",'Partido") + intToStr(i+1) + string("');");
        cout << query << endl;
    }
}

void insertarBloquePolitico(unsigned int cant){
    string query;
    unsigned int id = 1;
    for(unsigned int i = 0; i < cant; i++){
        query = string("insert into Bloque_politico (id_bloque_politico,nombre,id_partido_politico) values (") + intToStr(id) +  string(",'BloqueDiputados") + intToStr(i+1) + string("',") + intToStr(i+1) + string(");");
        cout << query << endl;
        query = string("insert into Bloque_politico (id_bloque_politico,nombre,id_partido_politico) values (") + intToStr(id+1) +  string(",'BloqueSenadores") + intToStr(i+1) + string("',") + intToStr(i+1) + string(");");
        cout << query << endl;
        id = id + 2;
    }
}

void insertarLegislador(){
    string query;
    string dnis[CANT_DNI];
    ifstream iArch;
    iArch.open("legisladores.csv");
    string linea;
    for(unsigned int i = 0; i < CANT_DNI; i++){
        //PRE: dnis suficientes en el archivo
        do{
            getline(iArch,linea);
        }while(!dniValido(linea) && !iArch.eof());
        dnis[i] = linea;
    }
    iArch.close();

    string d;
    unsigned int provi = 1;
    for(unsigned int i = 1; i <= CANT_SENADORES; i++){
        do{
            d = dnis[rand()%CANT_DNI];
        }while((conjDNI.end() != conjDNI.find(getDNI(d))) || d.length() == 0);
        conjDNI.insert(getDNI(d));
        conjSen.insert(d);
        query = string("insert into Legislador (dni, nombre, fecha_nacimiento,id_bloque_politico,provincia,tipo) values ('") + getDNI(d) + string("', '") + getNombre(d)+ string("', '") +  fechaAzar(1950,1982) + string("', ") + intToStr(bloqueSenadoresAzar(i,CANT_PARTIDOS)) + string(",'Provincia") + intToStr(provi) + "','S');";
        cout << query << endl;
        if((i)%3 == 0) provi = provi + 1;
    }

    //PRE: MAS PROVINCIAS QUE PARTIDOS POLITICOS

    for(unsigned int i = 0; i <= CANT_PROV; i++){
        while(habitantes[i] >= 33000){
            do{
                d = dnis[rand()%CANT_DNI];
            }while((conjDNI.end() != conjDNI.find(getDNI(d))) || d.length() == 0);
            conjDNI.insert(getDNI(d));
            conjDipu.insert(pair<string,string>(d,intToStr(i+1)));
            string bloque = intToStr(bloqueDiputadosAzar(i,CANT_PARTIDOS));
            if(bloque == "-1"){
                bloque = "1";
            }
            query = string("insert into Legislador (dni, nombre, fecha_nacimiento,id_bloque_politico,provincia,tipo) values ('") + getDNI(d) + string("', '") + getNombre(d)+ string("', '") +  fechaAzar(1950,1982) + string("',") + bloque + string(",'Provincia") + intToStr(i+1) + "','D');";
            cout << query << endl;
            habitantes[i] = habitantes[i] - 33000;
        }
    }

}

bool dniValido(string dni){
    if((dni.length() - dni.find("D.N.I") - 6) <= 1){
        return false;
    }
    else{
        if(dni.length() == 0)
            return false;
        else
            return true;
    }
}


string getDNI(string d){
    string res;
    unsigned int posDNI = d.find("D.N.I");
    if(posDNI == string::npos){
        cout << "ERROR(" << d.length() << "): " << d << endl;
        exit(1);
    }
    res = d.substr(posDNI+ 6,d.length() - posDNI - 7);
    return res;
}

string getNombre(string d){
    string res;
    unsigned int posDNI = d.find("D.N.I");
    if(posDNI == string::npos){
        cout << "ERROR(" << d.length() << "): " << d << endl;
        exit(1);
    }
    res = d.substr(0,posDNI-2);
    return res;
}

string fechaAzar(unsigned int minAnio, unsigned int maxAnio){
    return intToStr(minAnio+rand()%(maxAnio-minAnio)) + string("-") + intToStr(1+rand()%12) + string("-") + intToStr(1+rand()%30);
}

unsigned int bloqueSenadoresAzar(unsigned int it, unsigned int cantBloques){
    unsigned int res;
    if(it == 0){
        res = 2;
    }
    else{
        if(it <= cantBloques){
            res = 2* it;
        }
        else{
            res = 2 * (rand()%cantBloques) + 2;
            if(res > cantBloques * 2){
                res = cantBloques*2;
            }
        }
    }
    return res;
}

unsigned int bloqueDiputadosAzar(unsigned int it, unsigned int cantBloques){
    unsigned int res = 1;
    if(it <= cantBloques){
        res = 2 * (it-1) + 1;
    }
    else{
        res = 2 * ((rand()%cantBloques) + 1) - 1;
        if(res > (cantBloques * 2 - 1)){
            res = CANT_PARTIDOS*2-1;
        }
        if(res < 1){
            res = 1;
        }
    }
    return res;
}

void insertarCamaras(){
    string query;
    query = string("insert into Camara (id_camara,tipo) values (0,'D'), (1,'S');");
    cout << query << endl;
}

void insertarBieneEconomico(unsigned int valor, string tipo){
    string query;
    query = string("insert into Bien_economico (valor,tipo) values (") + intToStr(valor) + string(",'") + tipo + string("');");
    cout << query << endl;
}

void insertarBienes(){
    unsigned int idBien = 1;
    string query;
    //Por cada legislador
    for(set<string>::iterator it = conjDNI.begin(); it != conjDNI.end(); it++){
        string dniLegislador = *it;
        //Bienes inmobiliarios
        for(unsigned int i = 0; i <= rand()%10; i++){
            insertarBieneEconomico(100000+rand()%3000000,"I");
            query = string("insert into Bienes_del_legislador (dni_legislador,id_bien_economico,fecha_obtencion,fecha_sucesion) values ");
            query = query + string("('") + dniLegislador + string("',") + intToStr(idBien) + string(",'") + fechaAzar(1985,2014) + string("',NULL);");
            cout << query << endl;
            idBien++;
        }

        //Bienes de sociedad
        for(unsigned int i = 0; i < rand()%5; i++){
            insertarBieneEconomico(100000+rand()%5000000,"S");
            query = string("insert into Bienes_del_legislador (dni_legislador,id_bien_economico,fecha_obtencion,fecha_sucesion) values ");
            query = query + string("('") + dniLegislador + string("',") + intToStr(idBien) + string(",'") + fechaAzar(1985,2014) + string("',NULL);");
            cout << query << endl;
            idBien++;
        }

        //Bienes acciones
        for(unsigned int i = 0; i < rand()%5; i++){
            insertarBieneEconomico(100+rand()%5000,"A");
            query = string("insert into Bienes_del_legislador (dni_legislador,id_bien_economico,fecha_obtencion,fecha_sucesion) values ");
            query = query + string("('") + dniLegislador + string("',") + intToStr(idBien) + string(",'") + fechaAzar(1985,2014) + string("',NULL);");
            cout << query << endl;
            idBien++;
        }

    }
}

void insertarPeriodo(){
    string query;
    //Agrego un periodo
    query = string("insert into Periodo (fecha_inicio, fecha_fin) values ('2008-01-01','2012-12-31');");
    cout << query << endl;

    //Por cada legislador
    for(set<string>::iterator it = conjDNI.begin(); it != conjDNI.end(); it++){
        query = string("insert into Periodos_del_legislador (dni_legislador,fecha_inicio,fecha_fin) values ('") + (*it) + string("','2008-01-01','2012-12-31');");
        cout << query << endl;
    }
}

void insertarPartEnComisiones(){
    string query;
    //Aseguro que todos los dip están en al menos una comision
    unsigned int comision = 0;
    unsigned cantPresidencias = 0;
    for(set<pair<string, string> >::iterator it = conjDipu.begin(); it != conjDipu.end(); it++){
        string dniDipu = getDNI((*it).first);
        query = string("insert into Participa_en_comision (dni_legislador,fecha_inicio_participacion,fecha_fin_participacion,nombre_comision) values ('") + dniDipu + string("','2008-01-01','2012-12-31','Comision") + intToStr(comision+1) + string("');");
        cout << query << endl;
        if(cantPresidencias < CANT_COMISIONES){
            query = string("insert into Preside_comision (nombre_comision,dni_diputado,fecha_inicio_preside,fecha_fin_preside) values ('Comision") + intToStr(comision+1) + string("','") + dniDipu + string("','2008-01-01','2012-12-31');");
            cout << query << endl;
            cantPresidencias++;
        }
        for(unsigned int c = 1; c <= CANT_COMISIONES; c++){
            if(c == comision+1) continue;
            if(rand()%100 > 97){
                query = string("insert into Participa_en_comision (dni_legislador,fecha_inicio_participacion,fecha_fin_participacion,nombre_comision) values ('") + dniDipu + string("','2008-01-01','2012-12-31','Comision") + intToStr(c) + string("');");
                cout << query << endl;
            }
        }
        comision = (comision+1)%CANT_COMISIONES;
    }
}

void insertarVice(){
    string query;
    query = "insert into Vicepresidente (dni,nombre) values ('11222333','Amado Bodou');";
    cout << query << endl;
}

void insertarProyectos(){
    string query;
    string origen;
    for(unsigned int i = 1; i <= CANT_PROYECTOS; i++){
        if(rand()%100 > 50)
            origen = "D";
        else
            origen = "S";
        query = string("insert into Proyecto_de_ley (titulo_proyecto_ley,fecha,id_camara,estado_votaciones) values ('Proyecto") + intToStr(i) + string("','") + fechaAzar(2008,2009) + string("','") + origen + string("','A');");
        cout << query << endl;
    }
}

void insertarVoto(){
    string query;
    query = "insert into Voto (id_voto,resultado,tipo) values ('00','p','n'),('01','p','e'),('10','n','n'),('11','n','e'),('20','a','n'),('21','a','e');";
    cout << query << endl;
}

void insertarEstudia(){
    string query;
    for(unsigned int i = 1; i <= CANT_PROYECTOS; i++){
        for(unsigned int c = 1; c <= CANT_COMISIONES; c++){
            if(rand()%100 > 95){
                query = string("insert into Estudia (nombre_comision,titulo_proyecto_ley) values ('Comision") + intToStr(c) + string("','Proyecto") + intToStr(i) + string("');");
                cout << query << endl;
            }
        }
    }
}

void insertarPresideBloque(){
    string query;
    unsigned int bloque = 2;
    for(set<string>::iterator it = conjSen.begin(); it != conjSen.end(); it++){
        query = string("insert into Preside_bloque (dni_legislador,fecha_inicio_presidencia_bloque,fecha_fin_presidencia_bloque,id_bloque_politico) values ('") + getDNI(*it) + string("',2008-01-01','2012-12-31',") + intToStr(bloque) + string(");");
        cout << query << endl;
        bloque = bloque + 2;
        if(bloque > 12) break;
    }

    bloque = 1;
    for(set<pair<string,string> >::iterator it = conjDipu.begin(); it != conjDipu.end(); it++){
        query = string("insert into Preside_bloque (dni_legislador,fecha_inicio_presidencia_bloque,fecha_fin_presidencia_bloque,id_bloque_politico) values ('") + getDNI((*it).first) + string("',2008-01-01','2012-12-31',") + intToStr(bloque) + string(");");
        cout << query << endl;
        bloque = bloque + 2;
        if(bloque > 11) break;
    }
}

