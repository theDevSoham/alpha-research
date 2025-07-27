import PeopleList from "./components/PeopleList";

const App = () => {
  return (
    <div className="w-full min-h-10">
      <div className="max-w-2xl mt-10" style={{ margin: "auto" }}>
        <PeopleList />
      </div>
    </div>
  );
};

export default App;
