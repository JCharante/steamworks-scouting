import Vue from 'vue'
import Revue from 'revue'
import {createStore, combineReducers} from 'redux'
import actions from './actions/matches'

function matches (state = {matches: {}, matchKeys: []}, action) {
    switch (action.type) {
    case 'CREATE_MATCH':
        let newMatchData = {}
        newMatchData[action.payload.matchID] = action.payload
        // console.log('store.js: CREATE_MATCH >> newMatchData', newMatchData)

        return Object.assign({}, state, {
            matchKeys: [...state.matchKeys, action.payload.matchID],
            matches: Object.assign({}, state.matches, newMatchData)
        })
    case 'UPDATE_MATCH':
        let updatedMatchData = Object.assign({}, state.matches[action.payload.matchID], action.payload.dict)
        let bob = {}
        bob[action.payload.matchID] = updatedMatchData
        return Object.assign({}, state, {
            matches: Object.assign({}, state.matches, bob)
        })
    default:
        return state
    }
}

const reducers = combineReducers({
    matches
})

const reduxStore = createStore(reducers, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__())

const store = new Revue(Vue, reduxStore, actions)

export default store
