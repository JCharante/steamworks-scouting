export function createMatch (matchID) {
    return {
        type: 'CREATE_MATCH',
        payload: {
            matchID,
            eventName: null,
            matchNumber: null,
            teamNumber: null
        }
    }
}

export function updateMatch (matchID, dict) {
    return {type: 'UPDATE_MATCH', payload: {matchID, dict}}
}

export function fetchMatch (store, matchID) {
    return store.matches[matchID]
}

export default null
