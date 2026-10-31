



export type MorphologicalMethod =
    | 'stemming'
    | 'lemmatization'
    | 'none'


export type PreprocessResponse = {
    original_text: string
    normalized_text: string
    tokens: string[]
    filtered_tokens: string[]
    morphological_method: MorphologicalMethod
    morphological_tokens: string[]
    processed_text: string
}


export type PredictResponse = {
    prediction: {
        stars: number
        confidence: number
        probabilities: Record<string, number>
    }
    model: {
        name: string
        method: MorphologicalMethod
    }
}


//T representa el tipo de respuesta esperado en cada peticion
async function enviarResena<T>( endpoint: string, texto: string, ): Promise<T> {

    let respuesta: Response

    try {
        respuesta = await fetch(`/api/v1/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: texto }),
        })
    } catch {
        throw new Error(
            'No se pudo conectar con el servicio. Comprueba que esté iniciado.',
        )
    }

    if (!respuesta.ok) {
        const datos: {detail?: unknown} = await respuesta
            .json()
            .catch( () => ({}) )

        if (respuesta.status === 422 ) {
            throw new Error(
                'La reseña debe tener entre 3 y 5000 caracteres.',
            )
        }

        if (respuesta.status == 503) {
            throw new Error(
                typeof datos.detail === 'string'
                ? datos.detail
                : 'El servicio solicitado no está disponible.',
            )
        }

        throw new Error(
            `No se pudo completar la consulta. Código: ${respuesta.status}.`,
        )
    }

    return respuesta.json()
}


export function obtenerPreprocesamiento(texto: string) {
    return enviarResena<PreprocessResponse>('preprocess', texto)
}

export function obtenerPrediccion(texto: string) {
    return enviarResena<PredictResponse>('predict', texto)
}

