import java.util.ArrayList;
import java.util.HashMap;


public class StatementGenerator {
	
	public StatementGenerator(){} 
	
	public Integer Dni(){
		Integer randomNum=0 + (int)(Math.random()*4000000);
		return randomNum;
		
	}
	
	public Integer Edad(){
		Integer randomNum=18 + (int)(Math.random()*65);
		return randomNum;
		
		
	}
	
	public Integer salario(){
		Integer randomNum=2000 + (int)(Math.random()*20000);
		return randomNum;
		
		
	}
	
	
	
	
	public void crearTablaPersonas(){
		
		System.out.println(" CREATE TABLE personas( DNI INT PRIMARY KEY,nombre TEXT,apellido TEXT, edad TEXT );\" ");
	}
	

	public static void main(String args[]){
		
		//HashMap personas = new HashMap<Integer,Persona>();
		ArrayList<Persona> personas = new ArrayList<Persona>();
		
		StatementGenerator stm= new StatementGenerator();
		
		ArrayList<String> nombres = new ArrayList<String>();
		nombres.add("Martin");
		nombres.add("Sergio");
		nombres.add("Gino");
		nombres.add("Julian");
		nombres.add("Gabi");
		nombres.add("Foca");
		nombres.add("Pedro");
		nombres.add("Juan");
		nombres.add("Florencia");
		
		
		ArrayList<String> apellidos = new ArrayList<String>();
		apellidos.add("Celave");
		apellidos.add("Gonzalez");
		apellidos.add("Scarpino");
		apellidos.add("Dabah");
		apellidos.add("Croce");
		apellidos.add("Fernandez");
		apellidos.add("Molina");
		apellidos.add("Mendez");
		apellidos.add("Mazuce");
		
		ArrayList<String> departamentos = new ArrayList<String>();
		departamentos.add("ventas");
		departamentos.add("finanzas");
		departamentos.add("it");
		departamentos.add("marketing");
		
		
		stm.crearTablaPersonas();
		
		for(int i=0; i <nombres.size();i++){
			for(int j=0; j <apellidos.size();j++){
				
				Integer dni=stm.Dni();
				Persona p= new Persona(dni,nombres.get(i),apellidos.get(j),stm.Edad()) ;
				personas.add(p);
				
				/*String consulta=("INSERT INTO personas VALUES " +"(" +  stm.Dni()  + ","+"'" +nombres.get(i)+ "'"+", "+ "'" + apellidos.get(j) +"'"+", "+ stm.Edad()+") ");
				String statement = "statement.execute(" +"\" " + consulta+"\" "+")";
				System.out.println(statement);*/
			
				String consulta="\"INSERT INTO personas VALUES" + p.imprimirValorPersona();
				String statement="statement.execute("+consulta+"\")";
				System.out.println(statement);

			}	
		}
		
		for(int i =0; i<personas.size();i++ ){
			Persona p= personas.get(i);
			Integer dptNumber=0 + (int)(Math.random()*3);
			String personasYSalarios= "statement.execute("+ "\" INSERT INTO salarios VALUES("+
					p.getDni()+ ","+stm.salario()+","+"'"+ departamentos.get(dptNumber)+"'"+ ")"+"\""+ ")";
			
			System.out.println(personasYSalarios);
		}
		
		
		
		
		
		
		
	}

}
