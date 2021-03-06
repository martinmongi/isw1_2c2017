require './numero'

class Fraccion < Numero

  def initialize(numerador,denominador)
    @numerador = numerador
    @denominador = denominador
  end

  def numerador
    @numerador
  end

  def denominador
    @denominador
  end

  def es_cero
    false
  end

  def es_uno
    false
  end

  def == un_objeto
    (un_objeto.kind_of? self.class) && (self.igual_a_fraccion un_objeto)
  end

  def igual_a_fraccion(una_fraccion)
    (@numerador.multiplicar_por_un_entero una_fraccion.denominador) == (@denominador.multiplicar_por_un_entero una_fraccion.numerador)
  end

  def hash
    @numerador.hash
  end

  def mas_un_entero(un_entero)
    una_fraccion =  (@numerador.mas_un_entero @denominador.multiplicar_por_un_entero un_entero).dividir_por_un_entero (@denominador)
    return una_fraccion
    
  end

  def mas_una_fraccion(una_fraccion)
    return ((@numerador.multiplicar_por_un_entero una_fraccion.denominador).mas_un_entero @denominador.multiplicar_por_un_entero una_fraccion.numerador).dividir_por_un_entero (@denominador.multiplicar_por_un_entero una_fraccion.denominador)

  end

  def multiplicar_por_un_entero(un_entero)
    return (@numerador.multiplicar_por_un_entero un_entero).dividir_por_un_entero (@denominador)
  end
   
  def multiplicar_por_una_fraccion(una_fraccion)
    return (@numerador.multiplicar_por_un_entero una_fraccion.numerador).dividir_por_un_entero (@denominador.multiplicar_por_un_entero una_fraccion.denominador)
  end

  def dividir_por_un_entero(un_entero)

    una_fraccion = (@numerador).dividir_por_un_entero (@denominador.multiplicar_por_un_entero un_entero)
    return una_fraccion
  
  end

  def dividir_por_una_fraccion(una_fraccion)

    un_dividendo = self
    (un_dividendo.numerador.multiplicar_por_un_entero una_fraccion.denominador).dividir_por_un_entero (un_dividendo.denominador.multiplicar_por_un_entero una_fraccion.numerador)

  end

  def self.dividir(un_dividendo,un_divisor)
    return un_dividendo if un_dividendo.es_cero

    maximo_comun_divisor = un_dividendo.maximo_comun_divisor_con un_divisor
    nuevo_numerador = un_dividendo.divison_entera maximo_comun_divisor
    nuevo_denominador = un_divisor.divison_entera maximo_comun_divisor

    return nuevo_numerador if nuevo_denominador.es_uno

    self.new(nuevo_numerador,nuevo_denominador)
  end

end
