function Sidebar({ onNewChat }) {
  return <aside className="sidebar">
    <div className="brand-mark"><span className="brand-globe">◉</span><span>Briefly</span></div>
    <p className="brand-subtitle">THE WORLD, EXPLAINED</p>
    <button className="new-chat" onClick={onNewChat}><span>+</span> New conversation</button>
    <nav className="sidebar-nav">
      <p className="nav-label">EXPLORE</p>
      <button className="nav-item active">⌁ Today’s briefing</button>
      <button className="nav-item">◎ World</button>
      <button className="nav-item">⌁ Technology</button>
      <button className="nav-item">◒ Business</button>
      <button className="nav-item">◈ Culture & sport</button>
    </nav>
    <div className="sidebar-footer"><span className="live-dot" /> News sources updated live</div>
  </aside>;
}

export default Sidebar;
