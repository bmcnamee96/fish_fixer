import { FormMode } from './components/FormMode.jsx';
import { ChatMode } from './components/ChatMode.jsx';
import { PhotoMode } from './components/PhotoMode.jsx';

export function App() {
  return (
    <main>
      <h1>Fish Fixer</h1>
      <p>React + Node migration scaffold</p>
      <FormMode />
      <ChatMode />
      <PhotoMode />
    </main>
  );
}
