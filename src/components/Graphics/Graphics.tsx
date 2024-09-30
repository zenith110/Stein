import * as React from 'react'

import './Graphics.scss'
import output from '../../../output.png'


export default function Header() {
  return (
    <div className='graphics-container'>
      <img className='output' src={output} alt='pywebview'/>
      <h2>pywebview</h2>

      <div className='links'>
        <a href='https://pywebview.flowrl.com/' target='_blank'>Documentation</a>
      </div>
    </div>
  );
};
