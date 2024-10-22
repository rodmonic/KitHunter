// App.js
import React, { useState } from 'react';
import DataExplorer from './DataExplorer';
import KitLogForm from './KitLogForm';

import { SearchOutlined, UserOutlined, PlusOutlined } from '@ant-design/icons';
import { Layout, Menu } from 'antd';

const { Header, Sider, Content } = Layout;
// const { Panel } = Collapse;

const App = () => {
  const [selectedMenu, setSelectedMenu] = useState('1'); // Track selected menu item


  // Define content for each menu item
  const renderContent = () => {
    switch (selectedMenu) {
      case '1':
        return <div><KitLogForm /></div>;
      case '2':
        return <div><DataExplorer /></div>;
      case '3':
        return <div>User Stuff</div>;
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
          <Menu.Item key="add" onClick={() => setSelectedMenu('1')}>
            <PlusOutlined style={{ fontSize: '18px' }} />
          </Menu.Item>
          <Menu.Item key="search" onClick={() => setSelectedMenu('2')}>
            <SearchOutlined style={{ fontSize: '18px' }} />
          </Menu.Item>
          <Menu.Item key="profile" onClick={() => setSelectedMenu('3')}>
            <UserOutlined style={{ fontSize: '18px' }} />
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
