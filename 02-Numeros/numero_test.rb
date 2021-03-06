require 'minitest/autorun'
require 'minitest/reporters'
require './entero'
require './fraccion'

MiniTest::Reporters.use!

class NumberTest < Minitest::Test

  def setup
    @cero = Entero.new 0
    @uno = Entero.new 1
    @dos = Entero.new 2
    @tres = Entero.new 3
    @cuatro = Entero.new 4
    @cinco = Entero.new 5

    @unQuinto = @uno.dividir_por_un_entero @cinco
    @dosQuintos = @dos.dividir_por_un_entero @cinco
    @tresQuintos = @tres.dividir_por_un_entero @cinco
    @dosVeinticincoavos = @dos.dividir_por_un_entero (Entero.new 25)
    @unMedio = @uno.dividir_por_un_entero @dos
    @cincoMedios = @cinco.dividir_por_un_entero @dos
    @seisQuintos = (Entero.new 6).dividir_por_un_entero @cinco
    @cuatroMedios = @cuatro.dividir_por_un_entero @dos
    @dosCuartos = @dos.dividir_por_un_entero @cuatro
  end

  def test_01_es_cero_devuelve_true_solo_para_cero
    assert @cero.es_cero
    assert !@uno.es_cero
  end

  def test_02_es_uno_devuelve_true_solo_para_uno
    assert @uno.es_uno
    assert !@cero.es_uno
  end

  def test_03_suma_enteros_correctamente
    assert_equal @dos,(@uno.mas_un_entero @uno)
  end

  def test_04_multiplica_enteros_correctamente
    assert_equal @cuatro,(@dos.multiplicar_por_un_entero @dos)
  end

  def test_05_divide_enteros_correctamente
    assert_equal @uno,(@dos.dividir_por_un_entero @dos)
  end

  def test_06_suma_fracciones_correctamente
    sieteDecimos = nil # <- REEMPLAZAR POR LO QUE CORRESPONDA
    sieteDecimos = (Entero.new 7).dividir_por_un_entero (Entero.new 10)
    assert_equal sieteDecimos,(@unQuinto.mas_una_fraccion @unMedio)
    #
    # La suma de fracciones es:
    #
    # a/b + c/d = (a.d + c.b) / (b.d)
    #
    # SI ESTAN PENSANDO EN LA REDUCCION DE FRACCIONES NO SE PREOCUPEN!
    # TODAVIA NO SE ESTA TESTEANDO ESE CASO
  end

  def test_07_multiplica_fracciones_correctamente
    assert_equal @dosVeinticincoavos,(@unQuinto.multiplicar_por_una_fraccion @dosQuintos)
    #
    # La multiplicación de fracciones es:
    #
    # (a/b) * (c/d) = (a.c) / (b.d)
    #
    # SI ESTAN PENSANDO EN LA REDUCCION DE FRACCIONES NO SE PREOCUPEN!
    # TODAVIA NO SE ESTA TESTEANDO ESE CASO
    #
  end

  def test_08_divide_fracciones_correctamente
    assert_equal @cincoMedios,(@unMedio.dividir_por_una_fraccion @unQuinto)
    #
    # La división de fracciones es:
    #
    # (a/b) / (c/d) = (a.d) / (b.c)
    #
    # SI ESTAN PENSANDO EN LA REDUCCION DE FRACCIONES NO SE PREOCUPEN!
    # TODAVIA NO SE ESTA TESTEANDO ESE CASO
    #
  end

  #
  # Ahora empieza lo lindo! - Primero hacemos que se puedan sumar enteros con fracciones
  # y fracciones con enteros
  #
  def test_09_suma_enteros_con_fracciones_correctamente
    assert_equal @seisQuintos,(@uno.mas_una_fraccion @unQuinto)
  end

  def test_10_suma_fracciones_con_enteros_correctamente
    assert_equal @seisQuintos,(@unQuinto.mas_un_entero @uno)
  end

  #
  # Hacemos lo mismo para la multipliación
  #
  def test_11_multiplica_enteros_con_fracciones_correctamente
    assert_equal @dosQuintos,(@dos.multiplicar_por_una_fraccion @unQuinto)
  end

  def test_12_multiplica_fracciones_con_enteros_correctamente
    assert_equal @dosQuintos,(@unQuinto.multiplicar_por_un_entero @dos)
  end

  #
  # Hacemos lo mismo para la division
  #
  def test_13_divide_enteros_por_fracciones_correctamente
    assert_equal @cincoMedios,(@uno.dividir_por_una_fraccion @dosQuintos)
  end

  def test_14_divide_fracciones_por_enteros_correctamente
    assert_equal @dosVeinticincoavos,(@dosQuintos.dividir_por_un_entero @cinco)
  end

  #
  # Ahora si empezamos con problemas de reducción de fracciones
  #
  def test_15_fracciones_pueden_ser_iguales_a_enteros
    assert_equal @dos,@cuatroMedios
  end

  def test_16_las_fracciones_aparentes_son_iguales
    assert_equal @unMedio,@dosCuartos
    #
    # Las fracciones se reducen utilizando el maximo comun divisor (mcd)
    # Por lo tanto, para a/b, sea c = mcd (a,b) => a/b reducida es:
    # (a/c) / (b/c).
    #
    # Por ejemplo: a/b = 2/4 entonces c = 2. Por lo tanto 2/4 reducida es:
    # (2/2) / (4/2) = 1/2
    #
    # Para obtener el mcd pueden usar el algoritmo de Euclides que es:
    #
    # mcd (a,b) =
    # 		si b = 0 --> a
    # 		si b != 0 -->mcd(b, restoDeDividir(a,b))
    #
    # Ejemplo:
    # mcd(2,4) ->
    # mcd(4,restoDeDividir(2,4)) ->
    # mcd(4,2) ->
    # mcd(2,restoDeDividir(4,2)) ->
    # mcd(2,0) ->
    # 2
    #
  end

  def test_17_la_suma_de_fracciones_puede_dar_entero
    assert_equal @uno,(@unMedio.mas_una_fraccion @unMedio)
  end

  def test_18_la_multiplicacion_de_enteros_y_fracciones_puede_dar_entero
    assert_equal @dos,(@cuatro.multiplicar_por_una_fraccion @unMedio)
  end

  def test_19_la_division_de_enteros_puede_dar_fraccion
    assert_equal @unMedio,(@dos.dividir_por_un_entero @cuatro)
  end

  def test_20_la_division_de_fracciones_puede_dar_entero
    assert_equal @uno,(@unMedio.dividir_por_una_fraccion @unMedio)
  end

  def test_21_no_se_puede_dividir_enteros_por_cero
    assert_raises ZeroDivisionError do
      @uno.dividir_por_cero 
    end
  end

  def test_22_no_se_puede_dividir_fracciones_por_cero
    assert_raises ZeroDivisionError do
      @unQuinto.dividir_por_cero
    end
  end

end

