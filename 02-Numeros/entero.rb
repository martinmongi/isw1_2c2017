require './numero'

class Entero < Numero

  def initialize(value)
    @value = value
  end

  def es_cero
    @value == 0
  end

  def es_uno
    @value == 1
  end

  def value
    @value
  end

  def == un_objeto
    (un_objeto.kind_of? self.class) && (@value==un_objeto.value)
  end

  def hash
    @value.hash
  end

  def sumar_un_entero(un_entero)
    return Entero.new @value+un_entero.value
  end

  def sumar_una_fraccion(una_fraccion)
    un_numerador = Entero.new @value*una_fraccion.denominador.value+una_fraccion.numerador.value
    una_fraccion = Fraccion.dividir un_numerador,una_fraccion.denominador
    return una_fraccion
  end

  def *(un_multiplicador)
    if un_multiplicador.kind_of?(Entero)
      return Entero.new @value*un_multiplicador.value
    else
      un_numerador = Entero.new @value*un_multiplicador.numerador.value
      una_fraccion = Fraccion.dividir un_numerador,un_multiplicador.denominador
      return una_fraccion
     end
  end

  def /(un_divisor)
    if un_divisor.kind_of?(Entero)
      unDividendo = self
      Fraccion.dividir unDividendo,un_divisor
    else
      un_numerador = Entero.new @value*un_divisor.denominador.value
      una_fraccion = Fraccion.dividir un_numerador,un_divisor.numerador
      return una_fraccion
    end
  end

  def maximo_comun_divisor_con(otro_entero)
    if otro_entero.es_cero
      self
    else
      otro_entero.maximo_comun_divisor_con self.resto_con otro_entero
    end
  end

  def resto_con(un_divisor)
    Entero.new @value%un_divisor.value
  end

  def divison_entera(un_divisor)
    Entero.new @value/un_divisor.value
  end
end
