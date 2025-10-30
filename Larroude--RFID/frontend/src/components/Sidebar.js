import React from 'react';
import { 
  Home, 
  Tag, 
  Settings, 
  FileText, 
  Printer,
  BarChart3,
  Menu,
  X
} from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ activeTab, setActiveTab, isOpen, setIsOpen }) => {
  const menuItems = [
    {
      id: 'home',
      label: 'Início',
      icon: Home,
      description: 'Página inicial'
    },
    {
      id: 'labels',
      label: 'Etiquetas',
      icon: Tag,
      description: 'Geração de etiquetas'
    },
    {
      id: 'config',
      label: 'Configuração',
      icon: Settings,
      description: 'Config. impressora'
    },
    {
      id: 'reports',
      label: 'Relatórios',
      icon: BarChart3,
      description: 'Relatórios e logs'
    },
    {
      id: 'docs',
      label: 'Documentação',
      icon: FileText,
      description: 'Ajuda e docs'
    }
  ];

  const handleItemClick = (itemId) => {
    setActiveTab(itemId);
    // Fechar sidebar em mobile após seleção
    if (window.innerWidth <= 768) {
      setIsOpen(false);
    }
  };

  return (
    <>
      {/* Overlay para mobile */}
      {isOpen && (
        <div 
          className="sidebar-overlay"
          onClick={() => setIsOpen(false)}
        />
      )}
      
      {/* Sidebar */}
      <div className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        {/* Header */}
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <img src="/larroud-logo.svg" alt="Larroudé" className="logo-image" />
          </div>
          
          {/* Botão fechar (mobile) */}
          <button 
            className="sidebar-close-btn"
            onClick={() => setIsOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="sidebar-nav">
          <ul className="nav-list">
            {menuItems.map((item) => {
              const Icon = item.icon;
              return (
                <li key={item.id} className="nav-item">
                  <button
                    className={`nav-link ${activeTab === item.id ? 'nav-link-active' : ''}`}
                    onClick={() => handleItemClick(item.id)}
                  >
                    <div className="nav-icon">
                      <Icon size={20} />
                    </div>
                    <div className="nav-content">
                      <span className="nav-label">{item.label}</span>
                      <span className="nav-description">{item.description}</span>
                    </div>
                  </button>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Footer */}
        <div className="sidebar-footer">
          <div className="sidebar-version">
            <Printer size={16} />
            <span>Sistema RFID v1.0</span>
          </div>
          <div className="sidebar-status">
            <div className="status-indicator status-online"></div>
            <span>Sistema Online</span>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
