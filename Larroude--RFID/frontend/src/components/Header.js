import React from 'react';
import { Menu, Bell, User, Search } from 'lucide-react';
import './Header.css';

const Header = ({ sidebarOpen, setSidebarOpen, activeTab }) => {
  const getPageTitle = (tab) => {
    const titles = {
      home: 'Início',
      labels: 'Geração de Etiquetas',
      config: 'Configuração da Impressora',
      reports: 'Relatórios',
      docs: 'Documentação'
    };
    return titles[tab] || 'Sistema RFID Larroudé';
  };

  const getPageDescription = (tab) => {
    const descriptions = {
      home: 'Bem-vindo ao sistema de geração de etiquetas RFID',
      labels: 'Upload de CSV e geração de etiquetas personalizadas',
      config: 'Configuração e teste da impressora RFID',
      reports: 'Relatórios de impressão e estatísticas',
      docs: 'Documentação e ajuda do sistema'
    };
    return descriptions[tab] || 'Sistema profissional de etiquetas RFID';
  };

  return (
    <header className="app-header">
      <div className="header-left">
        {/* Menu toggle para mobile */}
        <button
          className="menu-toggle"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          <Menu size={20} />
        </button>

        {/* Título da página */}
        <div className="page-title-section">
          <h1 className="page-title">{getPageTitle(activeTab)}</h1>
          <p className="page-description">{getPageDescription(activeTab)}</p>
        </div>
      </div>

      <div className="header-right">
        {/* Barra de pesquisa */}
        <div className="search-bar">
          <Search size={16} />
          <input 
            type="text" 
            placeholder="Pesquisar..."
            className="search-input"
          />
        </div>

        {/* Notificações */}
        <button className="header-btn notification-btn">
          <Bell size={18} />
          <span className="notification-badge">2</span>
        </button>

        {/* Perfil do usuário */}
        <div className="user-profile">
          <button className="header-btn profile-btn">
            <User size={18} />
          </button>
          <div className="user-info">
            <span className="user-name">Usuário</span>
            <span className="user-role">Administrador</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
