import logo from './logo.svg';
import './App.css';
import GridComponent from './components/GridComponent';
import AppMenu from './components/AppMenu';
function App() {
  const gridData = [
    // Static grid data
  ];
  return (
    <div className="App">
      <header className="App-header">
       <AppMenu/>
      </header>
      <body>
        {/* Add your content here */}
        <p>This is the main content of my application.</p>
        <img src="your_image.jpg" alt="App image" />
        <GridComponent numColumns={3} /* Adjust as needed */>
          {/* ... Grid content if you're using the GridComponent ... */}
        </GridComponent>
      </body>
    </div>
  );
}

export default App;
