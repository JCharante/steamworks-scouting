export function setDefaultEvent (eventCode) {
    return { type: 'SET_DEFAULT_EVENT', payload: eventCode }
}

export function setScoutName (scoutName) {
    return { type: 'SET_SCOUT_NAME', payload: scoutName }
}

export function setServerPassword (serverPassword) {
    return { type: 'SET_SERVER_PASSWORD', payload: serverPassword }
}

export function setServerAddress (serverAddress) {
    return { type: 'SET_SERVER_ADDRESS', payload: serverAddress }
}

export default null
