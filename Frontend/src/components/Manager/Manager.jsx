import React, { useState } from 'react';
import './Modal.css';
import categoryConfig from './categoryConfig'; // Importar la configuración de categorías

const Modal = ({ isOpen, onClose, category }) => {
  const [step, setStep] = useState('selectAction'); // Mantiene el seguimiento de la parte del modal en la que se encuentra el usuario

  const handleClose = () => {
    setStep('selectAction'); // Restablece el paso al cerrar el modal
    onClose();
  };

  const renderContent = () => {
    if (step === 'selectAction') {
      return (
        <div>
          <h2>Gestionar {category}</h2>
          <button onClick={() => setStep('create')}>Crear {category}</button>
          <button onClick={() => setStep('modify')}>Modificar {category}</button>
          <button onClick={() => setStep('delete')}>Eliminar {category}</button>
        </div>
      );
    }

    console.log('category:', category);
    const fields = categoryConfig[category.toLowerCase()]?.[step];
    console.log('fields:', fields);

    if (!fields || fields.length === 0) {
      return (
        <div>
          <p>No se encontraron campos para {step} {category}.</p>
          <button onClick={() => setStep('selectAction')}>Atrás</button>
        </div>
      );
    }

    return (
      <div>
        <h2>{step === 'create' ? 'Crear' : step === 'modify' ? 'Modificar' : 'Eliminar'} {category}</h2>
        <form>
          {fields.map((field) => (
            <div key={field.key} className="form-row">
              <label>{field.label}:</label>
              <input type={field.type} placeholder={field.label} />
            </div>
          ))}
          <button type="submit">Enviar</button>
        </form>
        <button onClick={() => setStep('selectAction')}>Atrás</button>
      </div>
    );
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <button className="close-button" onClick={handleClose}>X</button>
        {renderContent()}
      </div>
    </div>
  );
};

const Manager = ({ category }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsModalOpen(true)}>Gestionar {category}</button>
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} category={category} />
    </div>
  );
};

export default Manager;
