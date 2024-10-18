// App.js
import React, { useState } from 'react';
import DataExplorer from './DataExplorer';

import { HomeOutlined, UserOutlined, SettingOutlined } from '@ant-design/icons';
import { Layout, Menu } from 'antd';
import {
  SearchOutlined,
  SkinOutlined,
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;
// const { Panel } = Collapse;

const App = () => {
  const [selectedMenu, setSelectedMenu] = useState('1'); // Track selected menu item


  // Define content for each menu item
  const renderContent = () => {
    switch (selectedMenu) {
      case '1':
        return <div>Home Content</div>;
      case '2':
        return <div>About Content</div>;
      case '3':
        return <div><DataExplorer /></div>;
      default:
        return <div>Home Content</div>;
    }
  };


  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Layout>
      <Header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div className="logo" style={{ color: '#fff', fontSize: '24px' }}>
          Kit Hunter
        </div>
        <Menu theme="dark" mode="horizontal" selectable={false} style={{ display: 'flex', gap: '20px' }}>
          <Menu.Item key="home" onClick={() => setSelectedMenu('1')}>
            <HomeOutlined style={{ fontSize: '18px' }} />
          </Menu.Item>
          <Menu.Item key="profile" onClick={() => setSelectedMenu('2')}>
            <UserOutlined style={{ fontSize: '18px' }} />
          </Menu.Item>
          <Menu.Item key="settings" onClick={() => setSelectedMenu('3')}>
            <SettingOutlined style={{ fontSize: '18px' }} />
          </Menu.Item>
        </Menu>
      </Header>
        <Content
          style={{
            margin: '24px 16px',
            padding: 24,
            background: '#fff',
            minHeight: 280,
            maxHeight: 'calc(100vh - 64px - 48px)',
            overflowY: 'auto'
          }}
        >
          {renderContent()}
        </Content>
      </Layout>
    </Layout>
  );
};

export default App;
