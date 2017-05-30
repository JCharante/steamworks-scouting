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

export function deleteInvalidMatches (store, matches) {
    let invalidMatchIDs = new Set()
    Object.keys(matches).forEach(function (key) {
        let match = matches[key]
        if (match.eventName === null || (match.matchNumber === '' || match.matchNumber === null) || (match.teamNumber === '' || match.teamNumber === null)) {
            invalidMatchIDs.add(match.matchID)
        }
    })
    invalidMatchIDs = Array.from(invalidMatchIDs)
    invalidMatchIDs.forEach(function (value) {
        store.dispatch(deleteMatch(value))
    })
}

export function fetchMatch (store, matchID) {
    return store.matches[matchID]
}

export function saveStoreToLocalStorage (store) {
    console.info('%cmatches.js: %cSaving Redux Store %O \'matches\' to Local Storage', 'color: blue', 'color: black', store)
    LocalStorage.set('matches', store)
}

export default null
