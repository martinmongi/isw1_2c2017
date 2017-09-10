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
    (@numerador*una_fraccion.denominador) == (@denominador*una_fraccion.numerador)
  end

  def hash
    @numerador.hash
  end

  def +(un_sumando)

    if un_sumando.kind_of?(Fraccion)
      return (@numerador*un_sumando.denominador+@denominador*un_sumando.numerador)/(@denominador*un_sumando.denominador)
    else
      una_fraccion =  (@numerador+@denominador*un_sumando)/(@denominador)
      return una_fraccion
    end
    
  end

  def *(un_multiplicador)
    if un_multiplicador.kind_of?(Fraccion)
      return (@numerador*un_multiplicador.numerador)/(@denominador*un_multiplicador.denominador)
    else
      una_fraccion = (@numerador*un_multiplicador)/(@denominador)
      return una_fraccion
    end
  end

  def /(un_divisor)
    if un_divisor.kind_of?(Fraccion)
      un_dividendo = self
      (un_dividendo.numerador*un_divisor.denominador)/(un_dividendo.denominador*un_divisor.numerador)
    else
      una_fraccion = (@numerador)/(@denominador*un_divisor)
      return una_fraccion
    end
  end

  def self.dividir(un_dividendo,un_divisor)
    raise ZeroDivisionError.new if un_divisor.es_cero
    return un_dividendo if un_dividendo.es_cero

    maximo_comun_divisor = un_dividendo.maximo_comun_divisor_con un_divisor
    nuevo_numerador = un_dividendo.divison_entera maximo_comun_divisor
    nuevo_denominador = un_divisor.divison_entera maximo_comun_divisor

    return nuevo_numerador if nuevo_denominador.es_uno

    self.new(nuevo_numerador,nuevo_denominador)
  end

end
