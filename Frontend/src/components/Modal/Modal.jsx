import React, { useState } from 'react';
import './Modal.css';

const Modal = ({ isOpen, onClose, category }) => {
  const [step, setStep] = useState('selectAction'); // Mantiene el seguimiento de la parte del modal en la que se encuentra el usuario

  const renderContent = () => {
    switch (step) {
      case 'selectAction':
        return (
          <div>
            <h2>Gestionar {category}</h2>
            <button onClick={() => setStep('create')}>Crear {category}</button>
            <button onClick={() => setStep('modify')}>Modificar {category}</button>
            <button onClick={() => setStep('delete')}>Eliminar {category}</button>
          </div>
        );
      case 'create':
        return (
          <div>
            <h2>Crear {category}</h2>
            <form>
              <input type="text" placeholder="Nombre" />
              <input type="text" placeholder="Apellido" />
              <input type="text" placeholder="CI" />
              <button type="submit">Enviar</button>
            </form>
            <button onClick={() => setStep('selectAction')}>Atrás</button>
          </div>
        );
      case 'modify':
        return (
          <div>
            <h2>Modificar {category}</h2>
            <form>
              <input type="text" placeholder={`CI de ${category} a modificar`} />
              <input type="text" placeholder="Nuevo Nombre" />
              <input type="text" placeholder="Nuevo Apellido" />
              <button type="submit">Enviar Cambios</button>
            </form>
            <button onClick={() => setStep('selectAction')}>Atrás</button>
          </div>
        );
      case 'delete':
        return (
          <div>
            <h2>Eliminar {category}</h2>
            <form>
              <input type="text" placeholder={`CI de ${category} a eliminar`} />
              <button type="submit">Eliminar</button>
            </form>
            <button onClick={() => setStep('selectAction')}>Atrás</button>
          </div>
        );
      default:
        return null;
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <button className="close-button" onClick={onClose}>X</button>
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
