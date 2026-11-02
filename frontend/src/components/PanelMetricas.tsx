import { useState } from "react";
import { obtenerMetricas, obtenerInfoModelo, obtenerExperimentos } from "../services/models";
import type { ExperimentRow, MetricsResponse, ModelInfoResponse } from "../services/models";



function porcentaje(valor: number): string {
    return `${(valor * 100).toFixed(2)} %`
}

function nombreMetodo(metodo: string): string {
    const nombres: Record<string, string> = {
        stemming: 'Stemming',
        lemmatization: 'Lemmatization',
        none: 'Sin transformacion morfologica',
    }

    return nombres[metodo] ?? metodo
}

function mensajeError(error: unknown): string {
    return error instanceof Error
        ? error.message
        : 'Ocurrio un error inesperdo.'
}

function PanelMetricas() {
    const [metricas, setMetricas] = useState<MetricsResponse | null>(null)
    const [modelo, setModelo] = useState<ModelInfoResponse | null>(null)
    const [experimentos, setExperimentos] = useState<ExperimentRow[] | null>(null)

    const [cargando, setCargando] = useState(false)
    const [errores, setErrores] = useState<string[]>([])

    async function cargarPanel() {
        setCargando(true)
        setErrores([])
        setMetricas(null)
        setModelo(null)
        setExperimentos(null)

        try {
            const [respuestaMetricas, respuestaModelo, respuestaExperimentos] = await Promise.allSettled([
                obtenerMetricas(),
                obtenerInfoModelo(),
                obtenerExperimentos(),
            ])

            const avisos: string[] = []

            if (respuestaMetricas.status === 'fulfilled') {
                setMetricas(respuestaMetricas.value)
            } else {
                avisos.push(
                    `Metricas: ${mensajeError(respuestaMetricas.reason)}`,
                )
            }

            if (respuestaModelo.status === 'fulfilled') {
                setModelo(respuestaModelo.value)
            } else {
                avisos.push(
                    `Modelo activo: ${mensajeError(respuestaModelo.reason)}`,
                )
            }

            if (respuestaExperimentos.status === 'fulfilled') {
                setExperimentos(respuestaExperimentos.value.experiments)
            } else {
                avisos.push(
                    `Experimentos: ${mensajeError(respuestaExperimentos.reason)}`,
                )
            }

            setErrores(avisos)
        } finally {
            setCargando(false)
        }
    }

    // Creamos una copia para ordenar sin modificar el estado.
    const experimentosOrdenados = [...(experimentos ?? [])].sort( 
        (a,b) => b.cv_macro_f1_mean - a.cv_macro_f1_mean, 
    )


    return (
        <section
            className="card border-0 shadow-sm mt-4"
            aria-labelledby="titulo-metricas"
        >
            <div className="card-body p-4">
                <h2 id="titulo-metricas" className="h5">
                    Evaluacion del modelo
                </h2>

                <p className="text-secondary">
                    Consulta los resultados del experimento final y su comparación con una línea base.
                </p>

                <button
                    type="button"
                    className="btn btn-outline-primary mb-4"
                    disabled={cargando}
                    onClick={() => void cargarPanel()}
                >
                    {cargando ? 'Consultando...' : 'Consultar metricas'}
                </button>

                <div aria-live="polite" aria-busy={cargando}>
                    {errores.length > 0 && (
                        <div className="alert alert-warning" role="alert">
                        <ul className="mb-0">
                            {errores.map((error) => (
                            <li key={error}>{error}</li>
                            ))}
                        </ul>
                        </div>
                    )}

                    {modelo && (
                        <div className="bg-light rounded p-3 mb-4">
                        <h3 className="h6">Modelo utilizado para predecir</h3>

                        <p className="mb-1">
                            {modelo.model_name}
                            {' · '}
                            {nombreMetodo(modelo.nlp_method)}
                        </p>

                        <p className="small text-secondary mb-0">
                            Versión: {modelo.model_version}.
                            {' '}Vectorizador: {modelo.vectorizer}.
                            {' '}N-gramas: {modelo.ngram_range.join('–')}.
                        </p>
                        </div>
                    )}

                    {metricas && (
                        <>
                        {modelo?.model_version !== 'final' && (
                            <div className="alert alert-warning">
                            Este informe corresponde al experimento final.
                            No se ha confirmado que el modelo activo
                            corresponda a ese mismo experimento.
                            </div>
                        )}

                        <h3 className="h6">Datos de la evaluación</h3>

                        <p>
                            Entrenamiento:
                            {' '}<strong>{metricas.train_size}</strong> reseñas.
                            {' '}Prueba:
                            {' '}<strong>{metricas.test_size}</strong> reseñas.
                        </p>

                        <p className="small text-secondary">
                            Configuración seleccionada:
                            {' '}{nombreMetodo(metricas.best_params.method)}.
                            {' '}N-gramas:
                            {' '}{metricas.best_params.ngram_range.join('–')}.
                            {' '}C: {metricas.best_params.C}.
                            {' '}Validación cruzada: {metricas.cv_folds} particiones.
                            {' '}Macro F1 de selección:
                            {' '}{porcentaje(metricas.best_cv_macro_f1)}.
                        </p>

                        <h3 className="h6 mt-4">
                            Comparación sobre el conjunto de prueba
                        </h3>

                        <div className="table-responsive">
                            <table className="table table-bordered align-middle">
                            <caption>
                                En Accuracy y Macro F1, un valor mayor es mejor.
                                En MAE, un valor menor es mejor.
                            </caption>

                            <thead>
                                <tr>
                                <th scope="col">Métrica</th>
                                <th scope="col">Línea base</th>
                                <th scope="col">Modelo del experimento final</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr>
                                <th scope="row">Accuracy</th>
                                <td>{porcentaje(metricas.baseline.accuracy)}</td>
                                <td>{porcentaje(metricas.final_test.accuracy)}</td>
                                </tr>

                                <tr>
                                <th scope="row">Macro F1</th>
                                <td>{porcentaje(metricas.baseline.macro_f1)}</td>
                                <td>{porcentaje(metricas.final_test.macro_f1)}</td>
                                </tr>

                                <tr>
                                <th scope="row">MAE</th>
                                <td>{metricas.baseline.mae.toFixed(3)}</td>
                                <td>{metricas.final_test.mae.toFixed(3)}</td>
                                </tr>
                            </tbody>
                            </table>
                        </div>

                        <ul className="small text-secondary">
                            <li>Accuracy: proporción de puntuaciones acertadas.</li>
                            <li>
                            Macro F1: promedio del F1 de las cinco clases,
                            dando el mismo peso a cada una.
                            </li>
                            <li>
                            MAE: diferencia absoluta promedio entre las
                            estrellas reales y las predichas.
                            </li>
                        </ul>

                        <h3 className="h6 mt-4">Matriz de confusión</h3>

                        <div className="table-responsive">
                            <table className="table table-bordered text-center">
                            <caption>
                                Filas: estrellas reales. Columnas: estrellas predichas.
                                La diagonal resaltada contiene los aciertos.
                            </caption>

                            <thead>
                                <tr>
                                <th scope="col">Real / Predicha</th>

                                {metricas.labels.map((etiqueta) => (
                                    <th key={etiqueta} scope="col">
                                    {etiqueta} ★
                                    </th>
                                ))}
                                </tr>
                            </thead>

                            <tbody>
                                {metricas.final_test.confusion_matrix.map(
                                (fila, indiceFila) => (
                                    <tr key={metricas.labels[indiceFila]}>
                                    <th scope="row">
                                        {metricas.labels[indiceFila]} ★
                                    </th>

                                    {fila.map((cantidad, indiceColumna) => (
                                        <td
                                        key={metricas.labels[indiceColumna]}
                                        className={
                                            indiceFila === indiceColumna
                                            ? 'table-success fw-semibold'
                                            : ''
                                        }
                                        >
                                        {cantidad}
                                        </td>
                                    ))}
                                    </tr>
                                ),
                                )}
                            </tbody>
                            </table>
                        </div>
                        </>
                    )}

                    {experimentos !== null && (
                        <>
                        <h3 className="h6 mt-4">
                            Comparación de configuraciones
                        </h3>

                        <p className="small text-secondary">
                            Resultados de validación cruzada sobre los datos
                            de entrenamiento, ordenados por Macro F1.
                            Estas cifras son distintas de la evaluación final
                            sobre el conjunto de prueba.
                        </p>

                        {experimentosOrdenados.length === 0 ? (
                            <p>No hay experimentos registrados.</p>
                        ) : (
                            <div className="table-responsive">
                            <table className="table table-striped align-middle">
                                <caption>
                                C es un parámetro de la regresión logística:
                                valores menores implican mayor regularización.
                                </caption>

                                <thead>
                                <tr>
                                    <th scope="col">Método</th>
                                    <th scope="col">N-gramas</th>
                                    <th scope="col">C</th>
                                    <th scope="col">Macro F1</th>
                                    <th scope="col">Accuracy</th>
                                    <th scope="col">MAE</th>
                                </tr>
                                </thead>

                                <tbody>
                                {experimentosOrdenados.map((experimento) => (
                                    <tr
                                    key={`${experimento.method}-${experimento.ngrams}-${experimento.C}`}
                                    >
                                    <td>{nombreMetodo(experimento.method)}</td>
                                    <td>{experimento.ngrams}</td>
                                    <td>{experimento.C}</td>
                                    <td>
                                        {porcentaje(experimento.cv_macro_f1_mean)}
                                    </td>
                                    <td>
                                        {porcentaje(experimento.cv_accuracy_mean)}
                                    </td>
                                    <td>
                                        {experimento.cv_mae_mean.toFixed(3)}
                                    </td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                            </div>
                        )}
                        </>
                    )}

                </div>
            </div>

        </section>
    )
}

export default PanelMetricas