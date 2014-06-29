
public class Persona {
	
	String nombre;
	String apellido;
	Integer edad;
	Integer dni;
	
	
	public Persona(Integer dni, String nombre, String apellido, Integer edad ) {
		this.nombre = nombre;
		this.apellido = apellido;
		this.edad = edad;
		this.dni = dni;
	}

	public String getNombre() {
		return nombre;
	}
	
	public void setNombre(String nombre) {
		this.nombre = nombre;
	}
	
	public String getApellido() {
		return apellido;
	}
	
	public void setApellido(String apellido) {
		this.apellido = apellido;
	}
	
	public Integer getEdad() {
		return edad;
	}
	
	public void setEdad(Integer edad) {
		this.edad = edad;
	}
	
	public Integer getDni() {
		return dni;
	}
	
	public void setDni(Integer dni) {
		this.dni = dni;
	}
	
	public String imprimirValorPersona(){
		String res= "("+dni+","+"'"+nombre+"'"+","+"'"+apellido+"'"+","+edad+")";
		return res;
		
	}
	

}
