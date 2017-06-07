import Vue from 'vue'
import Revue from 'revue'
import {LocalStorage} from 'quasar'
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
    case 'DELETE_MATCH':
        return Object.assign({}, state, {
            matchKeys: state.matchKeys.filter(matchID => matchID !== action.payload.matchID),
            matches: Object.keys(state.matches).reduce((result, matchID) => {
                if (matchID !== action.payload.matchID) {
                    result[matchID] = state.matches[matchID]
                }
                return result
            }, {})
        })
    default:
        return state
    }
}

function settings (state = {}, action) {
    switch (action.type) {
    case 'SET_DEFAULT_EVENT':
        return Object.assign({}, state, {
            defaultEvent: action.payload
        })
    case 'SET_SCOUT_NAME':
        return Object.assign({}, state, {
            scoutName: action.payload
        })
    case 'SET_SERVER_PASSWORD':
        return Object.assign({}, state, {
            serverPassword: action.payload
        })
    default:
        return state
    }
}

const reducers = combineReducers({ matches, settings })

let reduxStore = null

if (LocalStorage.get.item('store') === null) {
    console.info('%cstore.js: %cInitialized Store from Scratch', 'color: blue', 'color: black')
    reduxStore = createStore(reducers, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__())
}
else {
    console.info('%cstore.js: %cInitialized Store from Local Storage', 'color: blue', 'color: green')
    reduxStore = createStore(reducers, LocalStorage.get.item('store'), window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__())
}

export const store = new Revue(Vue, reduxStore, actions)

export function writeStoresToDisk () {
    let temporaryComponent = new Vue({
        methods: {
            fetchStores () {
                return { matches: this.$select('matches'), settings: this.$select('settings') }
            }
        }
    })
    LocalStorage.set('store', temporaryComponent.fetchStores())
}

export default store
