class Numero

  def subclass_responsibility
    raise Exception.new('Should be implemented by subclass')
  end

  def es_cero
    self.subclass_responsibility
  end

  def es_uno
    self.subclass_responsibility
  end

  def mas_un_entero(un_entero)
    self.subclass_responsibility
  end

  def mas_una_fraccion(una_fraccion)
    self.subclass_responsibility
  end

  def multiplicar_por_un_entero(un_entero)
    self.subclass_responsibility
  end

  def multiplicar_por_una_fraccion(una_fraccion)
    self.subclass_responsibility
  end

  def dividir_por_un_entero(un_entero)
    self.subclass_responsibility
  end
  
  def dividir_por_una_fraccion(una_fraccion)
    self.subclass_responsibility
  end

end
