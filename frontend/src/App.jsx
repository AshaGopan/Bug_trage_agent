import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import WatermarkBackground from './components/WatermarkBackground';

// Screen Components
import SignIn from './screens/SignIn';
import CreateAccount from './screens/CreateAccount';
import WorkspaceLanding from './screens/WorkspaceLanding';
import SplitViewSession from './screens/SplitViewSession';
import AnalyzingProgress from './screens/AnalyzingProgress';
import TriageResults from './screens/TriageResults';
import SuggestedResponse from './screens/SuggestedResponse';
import HistoryView from './screens/HistoryView';
import AccountSettings from './screens/AccountSettings';
import ComponentStatesView from './screens/ComponentStatesView';
import { AnalysisFailedCard } from './components/ErrorWarningCards';
import { INITIAL_SAMPLE_HISTORY } from './services/historyStorage';

export default function App() {
  // Theme Management (Light / Dark)
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('bug_triage_theme') || 'light';
  });

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('bug_triage_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [currentScreen, setCurrentScreen] = useState('workspace_landing');
  const [user, setUser] = useState({
    name: 'Alex Morgan',
    email: 'maintainer@k8s.io',
  });

  // Active triage session state
  const [activeInput, setActiveInput] = useState('');
  const [activeRepository, setActiveRepository] = useState('kubernetes/kubernetes');
  const [triageResult, setTriageResult] = useState(INITIAL_SAMPLE_HISTORY[1]); // Kubelet memory regression pre-populated
  const [missingInfo, setMissingInfo] = useState({
    stepsToReproduce: false,
    relevantLogs: false,
    environmentDetails: false,
  });
  const [analysisError, setAnalysisError] = useState(null);

  // Authentication Handlers
  const handleSignIn = (credentials) => {
    setUser((prev) => ({ ...prev, ...credentials }));
    setIsAuthenticated(true);
    setCurrentScreen('workspace_landing');
  };

  const handleSignUp = (newUser) => {
    setUser((prev) => ({ ...prev, ...newUser }));
    setIsAuthenticated(true);
    setCurrentScreen('workspace_landing');
  };

  const handleSignOut = () => {
    setIsAuthenticated(false);
    setCurrentScreen('signin');
  };

  // Triage Workflow Handlers
  const handleStartAnalysis = (input, repo = 'kubernetes/kubernetes') => {
    setActiveInput(input);
    setActiveRepository(repo);
    setAnalysisError(null);
    setCurrentScreen('analyzing');
  };

  const handleAnalysisComplete = (result) => {
    setTriageResult(result);
    setMissingInfo(result.missingInfo || {
      stepsToReproduce: false,
      relevantLogs: false,
      environmentDetails: false,
    });
    setCurrentScreen('results');
  };

  const handleAnalysisError = (errMsg) => {
    setAnalysisError(errMsg);
  };

  const handleToggleMissingInfo = (fieldKey) => {
    setMissingInfo((prev) => ({
      ...prev,
      [fieldKey]: !prev[fieldKey],
    }));
  };

  const handleViewHistoricalResult = (item) => {
    setTriageResult(item);
    setMissingInfo(item.missingInfo || {
      stepsToReproduce: false,
      relevantLogs: false,
      environmentDetails: false,
    });
    setCurrentScreen('results');
  };

  return (
    <div className="min-h-screen bg-[#F8F9FC] dark:bg-[#0B0F19] text-[#0F172A] dark:text-[#F8FAFC] relative flex flex-col font-sans selection:bg-indigo-100 dark:selection:bg-indigo-950 selection:text-[#2E31E8] dark:selection:text-indigo-300 transition-colors duration-200">
      {/* Subtle Background Watermark Graphic */}
      <WatermarkBackground />

      {/* Top Navigation Bar on Authenticated Screens */}
      {isAuthenticated && (
        <Navbar
          currentScreen={currentScreen}
          onNavigate={(screen) => setCurrentScreen(screen)}
          user={user}
          onSignOut={handleSignOut}
          theme={theme}
          onToggleTheme={toggleTheme}
        />
      )}

      {/* Main Screen Router */}
      <main className="flex-1">
        {/* Unauthenticated Screens */}
        {!isAuthenticated && currentScreen === 'signin' && (
          <SignIn
            onSignIn={handleSignIn}
            onSwitchToSignUp={() => setCurrentScreen('signup')}
            theme={theme}
            onToggleTheme={toggleTheme}
          />
        )}

        {!isAuthenticated && currentScreen === 'signup' && (
          <CreateAccount
            onSignUp={handleSignUp}
            onSwitchToSignIn={() => setCurrentScreen('signin')}
            theme={theme}
            onToggleTheme={toggleTheme}
          />
        )}

        {/* Authenticated Screens */}
        {isAuthenticated && (
          <>
            {currentScreen === 'workspace_landing' && (
              <WorkspaceLanding
                onStartAnalysis={(input) => handleStartAnalysis(input, 'kubernetes/kubernetes')}
                onOpenSplitView={() => setCurrentScreen('split_view')}
              />
            )}

            {currentScreen === 'split_view' && (
              <SplitViewSession
                onBackToLanding={() => setCurrentScreen('workspace_landing')}
                onStartAnalysis={(input, repo) => handleStartAnalysis(input, repo)}
              />
            )}

            {currentScreen === 'analyzing' && (
              <>
                {analysisError ? (
                  <div className="max-w-md mx-auto pt-16 px-4">
                    <AnalysisFailedCard onRetry={() => handleStartAnalysis(activeInput, activeRepository)} />
                  </div>
                ) : (
                  <AnalyzingProgress
                    input={activeInput}
                    repository={activeRepository}
                    onComplete={handleAnalysisComplete}
                    onError={handleAnalysisError}
                  />
                )}
              </>
            )}

            {currentScreen === 'results' && (
              <TriageResults
                result={triageResult}
                missingInfo={missingInfo}
                onToggleMissingInfo={handleToggleMissingInfo}
                onReviewResponse={() => setCurrentScreen('suggested_response')}
                onAnalyzeAnother={() => setCurrentScreen('workspace_landing')}
              />
            )}

            {currentScreen === 'suggested_response' && (
              <SuggestedResponse
                result={triageResult}
                missingInfo={missingInfo}
                onBackToResults={() => setCurrentScreen('results')}
              />
            )}

            {currentScreen === 'history' && (
              <HistoryView onViewResult={handleViewHistoricalResult} />
            )}

            {currentScreen === 'settings' && (
              <AccountSettings
                user={user}
                onUpdateUser={(updated) => setUser((prev) => ({ ...prev, ...updated }))}
                onSignOut={handleSignOut}
                theme={theme}
                onToggleTheme={toggleTheme}
              />
            )}

            {currentScreen === 'component_states' && (
              <ComponentStatesView
                onNavigateToWorkspace={() => setCurrentScreen('workspace_landing')}
                onNavigateToResults={() => setCurrentScreen('results')}
              />
            )}
          </>
        )}
      </main>
    </div>
  );
}
