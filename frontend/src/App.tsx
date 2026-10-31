import { useState } from "react";

import { obtenerPreprocesamiento, obtenerPrediccion } from "./services/reviews";
import type { PreprocessResponse, PredictResponse } from "./services/reviews";



const ETIQUETAS_METODO = {
  stemming: 'Raices mediante stemming',
  lemmatization: 'Lemas mediante lematizacion',
  none: 'sin transformacion morfologica'
}

function mensajeError(error: unknown): string {
  return error instanceof Error
    ? error.message
    : 'Ocurrio un error inesperado.'
}


// Reutilizamos este componente para cada lista de palabras.
function ListaTokens({ tokens }: { tokens: string[] }) {
  if (tokens.length === 0) {
    return <p className="text-secondary">No hay tokens en esta etapa.</p>
  }

  return (
    <ul className="list-unstyled d-flex flex-wrap gap-2">
      {tokens.map((token, indice) => (
        <li key={`${indice}-${token}`}>
          <span className="badge text-bg-secondary text-wrap">
            {token}
          </span>
        </li>
      ))}
    </ul>
  )
}


function App() {
  const [texto, setTexto] = useState('');
  // const [resultado, setResultado] = useState<PreprocessResponse | null>(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');

  const [preprocesamiento, setPreprocesamiento] = useState<PreprocessResponse | null>(null)

  const [prediccion, setPrediccion] = useState<PredictResponse | null>(null)

  const [errorPreprocesamiento, setErrorPreprocesamiento] = useState('')

  const [errorPrediccion, setErrorPrediccion] = useState('')

  
  function limpiarResultados() {
    setPreprocesamiento(null)
    setPrediccion(null)
    setError('')
    setErrorPreprocesamiento('')
    setErrorPrediccion('')
  }



  async function analizarResena() {
    const textoLimpio = texto.trim()

    limpiarResultados()

    if (textoLimpio.length < 3 || textoLimpio.length > 5000) {
      setError('La reseña debe tener entre 3 y 5000 caracteres')
      return
    }

    setCargando(true)

    try {
      // Ambas peticiones se ejecutan en paralelo.
      // Si una falla, todavía podemos mostrar la otra.
      const [respuestaNlp, respuestaPrediccion] = await Promise.allSettled([
        obtenerPreprocesamiento(textoLimpio),
        obtenerPrediccion(textoLimpio),
      ])

      if (respuestaNlp.status === 'fulfilled') {
        setPreprocesamiento(respuestaNlp.value)
      } else {
        setErrorPreprocesamiento(
          mensajeError(respuestaNlp.reason),
        )
      }

      if (respuestaPrediccion.status === 'fulfilled') {
        setPrediccion(respuestaPrediccion.value)
      } else {
        setErrorPrediccion(
          mensajeError(respuestaPrediccion.reason),
        )
      }

    } finally {
      setCargando(false)
    }
  }

  // La API devuelve los tokens originales y los conservados.
  // La diferencia permite visualizar cuáles fueron eliminados.
  const tokensConservados = new Set(
    preprocesamiento?.filtered_tokens ?? [],
  )

  const tokensEliminados = (
    preprocesamiento?.tokens ?? []
  ).filter((token) => !tokensConservados.has(token))


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
                  void analizarResena()
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
                  value={texto}
                  disabled={cargando}
                  aria-describedby="ayuda-resena"
                  placeholder="Ejemplo: No me gustó la batería, pero la pantalla es excelente."
                  onChange={(event) => {
                    setTexto(event.target.value)
                    limpiarResultados()
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
                  {cargando ? 'Analizando...' : 'Analizar reseña'}
                </button>
              </form>
            </div>
          </section>

          <div aria-live="polite" aria-busy={cargando}>
            {errorPrediccion && (
              <div className="alert alert-warning" role="alert">
                <strong>No se pudo obtener la prediccion</strong>
                {''}{errorPrediccion}
              </div>
            )}

            {prediccion && (
              <section
                className="card border-0 shadow-sm mb-4"
                aria-labelledby="titulo-prediccion"
              >
                <div className="card-body p-4">
                  <h2 id="titulo-prediccion" className="h5 mb-4">
                    Puntuacion estimada
                  </h2>

                  <div
                    className="fs-2 text-warning"
                    aria-hidden="true"
                  >
                    {'★'.repeat(prediccion.prediction.stars)}
                    {'☆'.repeat(5 - prediccion.prediction.stars)}
                  </div>

                  <p className="fw-semibold">
                    {prediccion.prediction.stars} de 5 estrellas
                  </p>

                  <p>
                    Probabilidad de esta puntuacion:
                    {' '}
                    <strong>
                      {(prediccion.prediction.confidence * 100).toFixed(1)} %
                    </strong>
                  </p>

                  <h3 className="h6 mt-4">
                    Probabilidad por puntuacion
                  </h3>

                  {Object.entries(
                      prediccion.prediction.probabilities,
                    ).sort(([a], [b]) => Number(a) - Number(b))
                    .map(([estrellas, probabilidad]) => (
                      <div key={estrellas} className="mb-2">
                        <div className="d-flex justify-content-between">
                          <span>
                            {estrellas}
                            {' '}
                            {estrellas === '1'
                              ? 'estrella'
                              : 'estrellas'
                            }
                          </span>

                          <span>
                            {(probabilidad * 100).toFixed(1)} %
                          </span>
                        </div>

                        <progress
                          className="w-100"
                          max={1}
                          value={probabilidad}
                          aria-label={`Probabilidad de ${estrellas} estrellas`}
                        />
                      </div>
                  ))}

                  <p className="small text-secondary mt-3 mb-0">
                    Modelo: {prediccion.model.name}.
                    {' '}
                    {ETIQUETAS_METODO[prediccion.model.method]}.
                  </p>

                </div>
              </section>
            )}

            {errorPreprocesamiento && (
              <div className="alert alert-warning" role="alert">
                <strong>No se pudo obtener el preprocesamiento</strong>
                {' '}{errorPreprocesamiento}
              </div>
            )}

            {preprocesamiento && (
              <section
                className="card border-0 shadow-sm"
                aria-labelledby="titulo-preprocesamiento"
              >
                <div className="card-body p-4">
                  <h2
                    id="titulo-preprocesamiento"
                    className="h5 mb-4"
                  >
                    Preprocesamiento paso a paso
                  </h2>

                  <h3 className="h6">1. Texto original</h3>
                  <p className="texto-resena bg-light rounded p-3">
                    {preprocesamiento.original_text}
                  </p>

                  <h3 className="h6">2. Texto normalizado</h3>
                  <p className="texto-resena bg-light rounded p-3">
                     {preprocesamiento.normalized_text}
                  </p>

                  <h3 className="h6">
                    3. Tokens ({preprocesamiento.tokens.length})
                  </h3>
                  <ListaTokens tokens={preprocesamiento.tokens} />

                  <h3 className="h6">
                    4. Stop words eliminadas
                    {' '}({tokensEliminados.length})
                  </h3>

                   {tokensEliminados.length > 0 ? (
                    <ListaTokens tokens={tokensEliminados} />
                  ) : (
                    <p className="text-secondary">
                      No se eliminaron stop words.
                    </p>
                  )}

                  <h3 className="h6">5. Tokens sin stop words</h3>
                  <ListaTokens
                    tokens={preprocesamiento.filtered_tokens}
                  />

                  <h3 className="h6">
                    6. {ETIQUETAS_METODO[
                      preprocesamiento.morphological_method
                    ]}
                  </h3>
                  <ListaTokens
                    tokens={preprocesamiento.morphological_tokens}
                  />

                  <h3 className="h6">
                    7. Texto final para el vectorizador TF-IDF
                  </h3>
                  <p className="texto-resena bg-light rounded p-3 mb-0">
                    {preprocesamiento.processed_text ||
                      'El procesamiento produjo un texto vacío.'}
                  </p>

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