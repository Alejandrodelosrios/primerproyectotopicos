


export type EvaluationMetrics = {
    accuracy: number
    macro_f1: number
    mae: number
    confusion_matrix: number[][]
}

export type MetricsResponse = {
    created_at: string | null
    selection_rule: string
    best_params: {
        method: string
        ngram_range: number[]
        C: number
    }
    best_cv_macro_f1: number
    cv_folds: number
    train_size: number
    test_size: number
    labels: number[]
    baseline: EvaluationMetrics
    final_test: EvaluationMetrics
}


export type ModelInfoResponse = {
    model_name: string
    model_version: string
    nlp_method: string
    vectorizer: string
    ngram_range: number[]
    classes: number[]
    artifact_path: string
}

export type ExperimentRow = {
    method: string
    ngrams: string
    C: number
    cv_macro_f1_mean: number
    cv_macro_f1_std: number
    cv_accuracy_mean: number
    cv_mae_mean: number
}

type ExperimentsResponse = {
    experiments: ExperimentRow[]
}

async function consultarModelo<T>(endpoint: string): Promise<T> {
    let respuesta: Response

    try {
        respuesta = await fetch(`/api/v1/models/${endpoint}`)
    } catch {
        throw new Error (
            'No se pudo conectar con el servicio. Comprueba que esté iniciado.',
        )
    }

    if (!respuesta.ok) {
        if (respuesta.status === 404)
            throw new Error('No hay resultados de entrenamiento disponibles.')
        
        if (respuesta.status === 503)
            throw new Error('El modelo de predicción no está disponible.')
        
        throw new Error(
            `No se pudo completar la consulta. Código: ${respuesta.status}.`,
        )
    }

    return respuesta.json()
}

export function obtenerMetricas() {
    return consultarModelo<MetricsResponse>('metrics')
}

export function obtenerInfoModelo() {
    return consultarModelo<ModelInfoResponse>('info')
}

export function obtenerExperimentos() {
    return consultarModelo<ExperimentsResponse>('experiments')
}