import java.util.ArrayList;


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
	
	
	public void crearTablaPersonas(){
		
		System.out.println(" CREATE TABLE personas( DNI INT PRIMARY KEY,nombre TEXT,apellido TEXT, edad TEXT );\" ");
	}
	

	public static void main(String args[]){
		
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
		
		
		//ArrayList<String> completos = new ArrayList<String>();
		
		//Integer[] edades ={ 23, 24, 25, 31, 58,42,29,30,33,61,35,52};	
		
		stm.crearTablaPersonas();
		
		for(int i=0; i <nombres.size();i++){
			for(int j=0; j <apellidos.size();j++){
			
				String consulta=("INSERT INTO personas VALUES " +"(" +  stm.Dni()  + ","+" '" +nombres.get(i)+ "'"+", "+ "'" + apellidos.get(j) +"'"+", "+ stm.Edad()+") ");
				String statement = "statement.execute(" +"\" " + consulta+"\" "+")";
				System.out.println(statement);
			}
			
			
		}
		
		
		
		
		
		
		
	}

}
