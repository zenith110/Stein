import * as React from 'react'
import './Graphics.scss'


export default function Graphics() {
  const [fileIndex, setFileIndex] = React.useState(1)
  const [hideFileIndexComboBox, setHideFileIndexComboBox] = React.useState(true)
  const [selectedOption, setSelectedOption] = React.useState("Cards")
  const [open, setOpen] = React.useState(false)
  const [imageData, setImageData] = React.useState<string | null>(null)

  const handleClickOpen = () => {
    window.pywebview.api.open_file_dialog()
    setOpen(true)
  }

  const handleClose = () => {
    setOpen(false)
  }

  const handleSubmit = () => {
    setOpen(false)
    setHideFileIndexComboBox(false)
  }

  const handleFinalSubmit = async () => {
    try {
      const result = await window.pywebview.api.select_graphics(selectedOption, fileIndex)
      setImageData(result)
    } catch (error) {
      console.error("Error processing graphics:", error)
    }
  }

  return (
    <div className='graphics-container'>
      <h2>pywebview</h2>
      <div className='controls'>
        <div className='open-file-container'>
          <button className='btn primary' onClick={handleClickOpen}>Open File</button>
        </div>
        {!hideFileIndexComboBox && (
          <div className='file-index-group'>
            <label htmlFor='file-index'>File Index:</label>
            <select 
              id='file-index'
              value={fileIndex} 
              onChange={(e) => setFileIndex(Number(e.target.value))}
            >
              {[...Array(820)].map((_, i) => (
                <option key={i + 1} value={i + 1}>
                  {i + 1}
                </option>
              ))}
            </select>
            <button className='btn secondary' onClick={handleFinalSubmit}>Submit</button>
          </div>
        )}
      </div>
      {imageData && (
        <div className='image-container'>
          <img src={imageData} alt='Selected Graphics' />
        </div>
      )}
      {open && (
        <div className='modal-overlay'>
          <div className='modal'>
            <h3>Which graphics would you like to load?</h3>
            <div className='radio-group'>
              <label>
                <input
                  type='radio'
                  value='Cards'
                  checked={selectedOption === 'Cards'}
                  onChange={(e) => setSelectedOption(e.target.value)}
                />
                Cards
              </label>
              <label>
                <input
                  type='radio'
                  value='Packs'
                  checked={selectedOption === 'Packs'}
                  onChange={(e) => setSelectedOption(e.target.value)}
                />
                Packs
              </label>
            </div>
            <div className='modal-actions'>
              <button className='btn secondary' onClick={handleClose}>Cancel</button>
              <button className='btn primary' onClick={handleSubmit}>Submit</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
