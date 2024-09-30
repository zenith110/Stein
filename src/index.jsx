import React from 'react'
import ReactDOM from 'react-dom'

import Graphics from './components/Graphics/Graphics'

import './index.scss'

const App = function() {
  return (
    <>
      <Graphics/>
    </>
  )
}

const view = App('pywebview')

const element = document.getElementById('app')
ReactDOM.render(view, element)