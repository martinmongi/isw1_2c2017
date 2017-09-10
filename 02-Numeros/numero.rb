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

  def +(un_sumando)
    self.subclass_responsibility
  end

  def *(un_multiplicador)
    self.subclass_responsibility
  end

  def /(un_divisor)
    self.subclass_responsibility
  end

end
