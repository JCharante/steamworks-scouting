import {LocalStorage} from 'quasar'

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

export function deleteMatch (matchID) {
    return {type: 'DELETE_MATCH', payload: {matchID}}
}

export function fetchMatch (store, matchID) {
    return store.matches[matchID]
}

export function saveStoreToLocalStorage (store) {
    console.info('%cmatches.js: %cSaving Redux Store %O \'matches\' to Local Storage', 'color: blue', 'color: black', store)
    LocalStorage.set('matches', store)
}

export default null
