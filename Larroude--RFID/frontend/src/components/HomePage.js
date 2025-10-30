import React from 'react';
import { Tag, Printer, BarChart3, Settings, ArrowRight, CheckCircle } from 'lucide-react';
import './HomePage.css';

const HomePage = ({ setActiveTab }) => {
  const quickActions = [
    {
      id: 'labels',
      title: 'Gerar Etiquetas',
      description: 'Upload CSV e impressão de etiquetas RFID',
      icon: Tag,
      color: 'blue',
      action: () => setActiveTab('labels')
    },
    {
      id: 'config',
      title: 'Configurar Impressora',
      description: 'Testar conexão e configurações',
      icon: Printer,
      color: 'green',
      action: () => setActiveTab('config')
    },
    {
      id: 'reports',
      title: 'Ver Relatórios',
      description: 'Estatísticas e logs de impressão',
      icon: BarChart3,
      color: 'purple',
      action: () => setActiveTab('reports')
    }
  ];

  const systemFeatures = [
    'Upload de arquivos CSV',
    'Geração automática de etiquetas',
    'Impressão individual com controle de quantidade',
    'Layout profissional da Larroud',
    'Sistema sem VOID garantido',
    'Interface moderna e responsiva'
  ];

  const recentStats = [
    { label: 'Etiquetas impressas hoje', value: '0', color: 'blue' },
    { label: 'Última impressão', value: 'Nunca', color: 'green' },
    { label: 'Status da impressora', value: 'Online', color: 'green' },
    { label: 'Economia de material', value: '100%', color: 'purple' }
  ];

  return (
    <div className="home-page">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Sistema RFID <span className="text-gradient">Larroudé</span>
          </h1>
          <p className="hero-description">
            Geração profissional de etiquetas RFID com layout otimizado, 
            controle de quantidade e máxima economia de material.
          </p>
          <button 
            className="hero-cta"
            onClick={() => setActiveTab('labels')}
          >
            Começar Agora
            <ArrowRight size={18} />
          </button>
        </div>
        <div className="hero-image">
          <div className="floating-card">
            <Tag size={24} />
            <span>Etiquetas RFID</span>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2 className="section-title">Ações Rápidas</h2>
        <div className="actions-grid">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <button
                key={action.id}
                className={`action-card action-${action.color}`}
                onClick={action.action}
              >
                <div className="action-icon">
                  <Icon size={24} />
                </div>
                <div className="action-content">
                  <h3 className="action-title">{action.title}</h3>
                  <p className="action-description">{action.description}</p>
                </div>
                <ArrowRight size={16} className="action-arrow" />
              </button>
            );
          })}
        </div>
      </div>

      {/* Stats Grid */}
      <div className="stats-section">
        <h2 className="section-title">Estatísticas do Sistema</h2>
        <div className="stats-grid">
          {recentStats.map((stat, index) => (
            <div key={index} className={`stat-card stat-${stat.color}`}>
              <div className="stat-value">{stat.value}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <div className="features-section">
        <h2 className="section-title">Funcionalidades</h2>
        <div className="features-grid">
          {systemFeatures.map((feature, index) => (
            <div key={index} className="feature-item">
              <CheckCircle size={16} className="feature-icon" />
              <span>{feature}</span>
            </div>
          ))}
        </div>
      </div>

      {/* System Status */}
      <div className="status-section">
        <div className="status-card">
          <div className="status-header">
            <h3>Status do Sistema</h3>
            <div className="status-indicator online"></div>
          </div>
          <div className="status-info">
            <p>✅ Servidor backend operacional</p>
            <p>✅ Impressora conectada e pronta</p>
            <p>✅ Template otimizado carregado</p>
            <p>✅ Sistema sem VOID funcionando</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
