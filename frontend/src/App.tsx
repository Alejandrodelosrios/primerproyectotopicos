import { useState } from "react";



// representa respuesta que devuelve el backend
type PreprocessResponse = {
  original_text: string
  normalized_text: string
  tokens: string[]
}


function App() {

  const [texto, setTexto] = useState('');
  const [resultado, setResultado] = useState<PreprocessResponse | null>(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');


  async function procesarResena() {
    const textoLimpio = texto.trim()

    setError('')
    setResultado(null)

    if (textoLimpio.length < 3 || textoLimpio.length > 5000) {
      setError('La reseña debe tener entre 3 y 5000 caracteres')
      return
    }

    setCargando(true)

    try {
      const respuesta = await fetch('/api/v1/preprocess', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textoLimpio }),
      })

      if (!respuesta.ok) {

        if (respuesta.status === 422)
          throw new Error( 'El servidor rechazo el texto. Revisa su contenido.', )
      
        throw new Error(`No se pudo procesar la reseña. Codigo: ${respuesta.status}.`,)
      }

      const datos: PreprocessResponse = await respuesta.json()
      setResultado(datos)

    } catch (error) {
      setError(
        error instanceof TypeError
        ? 'No se pudo conectar con el servicio. Comprueba que esté iniciado.'
        : error instanceof Error
            ? error.message
            : 'Ocurrio un error inesperado',
      )
    } finally {
      setCargando(false)
    }
  }


  return (

    <main className="container py-5">
      <div className="row justify-content-center">
        <div className="col-12 col-lg-8">
          <header className="mb-4">
            <h1 className="h2">Analisis de reseñas</h1>
            <p className="text-secondary">
              Escribe una reseña para explorar cómo se prepara
              su texto antes de realizar una predicción.
            </p>
          </header>

          <section
            className="card border-0 shadow-sm mb-4"
            aria-labelledby="titulo-formulario"
          >
            <div className="card-body p-4">
              <h2 id="titulo-formulario" className="h5 mb-3">
                Ingresa tu reseña
              </h2>

              <form
                noValidate
                onSubmit={(event) => {
                  event.preventDefault()
                  void procesarResena()
                }}
              >
                <label htmlFor="resena" className="form-label">
                  Reseña del producto
                </label>

                <textarea 
                  id="resena"
                  className="form-control"
                  rows={5}
                  maxLength={5000}
                  placeholder="Ejemplo: No me gustó la batería, pero la pantalla es excelente."
                  value={texto}
                  disabled={cargando}
                  aria-describedby="ayuda-resena"
                  onChange={(event) => {
                    setTexto(event.target.value)
                    setResultado(null)
                    setError('')
                  }}
                />

                <div id="ayuda-resena" className="form-text mb-3">
                  Entre 3 y 5000 caracteres.
                  {' '}Escritos: {texto.length}/5000.
                </div>

                {error && (
                  <div className="alert alert-danger" role="alert">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={cargando}
                >
                  {cargando ? 'Procesando...' : 'Procesar reseña'}
                </button>
              </form>
            </div>
          </section>

          <div aria-live="polite" aria-busy={cargando}>
            {resultado && (
              <section
                className="card border-0 shadow-sm"
                aria-labelledby="titulo-resultados"
              >
                <div className="card-body p-4">
                  <h2 id="titulo-resultados" className="h5 mb-4">
                    Resultado del preprocesamiento
                  </h2>

                  <h3 className="h6">1. Texto original</h3>
                  <p className="texto-resena bg-light rounded p-3">
                    {resultado.original_text}
                  </p>

                  <h3 className="h6">2. Texto normalizado</h3>
                  <p className="texto-resena bg-light rounded p-3">
                     {resultado.normalized_text}
                  </p>

                  <h3 className="h6">
                    3. Tokens ({resultado.tokens.length})
                  </h3>

                  {resultado.tokens.length > 0 ? (
                    <ul className="list-unstyled d-flex flex-wrap gap-2 mb-0">
                      {resultado.tokens.map((token, indice) => (
                        <li key={`${indice}-${token}`}>
                          <span className="badge text-bg-secondary text-wrap">
                            {token}
                          </span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-secondary mb-0">
                      El procesamiento no produjo tokens.
                    </p>
                  )}
                </div>
              </section>
            )}
          </div>


        </div>
      </div>
    </main>
  )
}

export default App