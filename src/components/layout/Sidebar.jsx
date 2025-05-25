import { useState, useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import {
  X,
  LayoutDashboard,
  Upload,
  MessageSquare,
  Clock,
  Settings,
  ChevronLeft,
  ChevronRight,
  Menu,
  Plus,
} from "lucide-react";
import useStore from "../../store/useStore";

function Sidebar({ open, onClose }) {
  const { t } = useTranslation();
  const location = useLocation();
  const navigate = useNavigate();
  const store = useStore();
  const [collapsed, setCollapsed] = useState(() => {
    // Get initial state from localStorage
    const savedState = localStorage.getItem("sidebarCollapsed");
    return savedState ? JSON.parse(savedState) : false;
  });
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  const isActive = (path) => location.pathname === path;

  const handleNewChat = () => {
    const newConversation = {
      id: Date.now(),
      title: "New Conversation",
      messages: [],
    };
    store.setCurrentConversation(newConversation);
    navigate("/chat");
  };

  // Save collapsed state to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem("sidebarCollapsed", JSON.stringify(collapsed));
  }, [collapsed]);

  const links = [
    {
      path: "/",
      label: t("nav.dashboard"),
      icon: <LayoutDashboard size={20} />,
    },
    { path: "/import", label: t("nav.import"), icon: <Upload size={20} /> },
    { path: "/chat", label: t("nav.chat"), icon: <MessageSquare size={20} /> },
    { path: "/history", label: t("nav.history"), icon: <Clock size={20} /> },
    {
      path: "/settings",
      label: t("nav.settings"),
      icon: <Settings size={20} />,
    },
  ];

  // Handle responsive behavior
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
      // Reset collapsed state when going from mobile to desktop
      if (window.innerWidth >= 768 && open) {
        onClose();
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [open, onClose]);

  return (
    <>
      {/* Mobile overlay */}
      {open && isMobile && (
        <div className="fixed inset-0 z-40" onClick={onClose}>
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75"></div>
        </div>
      )}

      <aside
        className={`fixed md:sticky top-0 left-0 z-50 h-full md:h-[calc(100vh-4rem)] 
                  ${
                    isMobile
                      ? open
                        ? "translate-x-0"
                        : "-translate-x-full"
                      : "translate-x-0"
                  }
                  ${collapsed && !isMobile ? "w-16" : "w-64"}
                  bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 overflow-y-auto flex-shrink-0
                  transition-all duration-200 ease-in-out`}
      >
        <div className="p-4 flex flex-col h-full">
          <div className="flex items-center justify-between mb-4">
            {isMobile ? (
              <button
                onClick={onClose}
                className="p-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                <X size={20} />
              </button>
            ) : (
              <button
                onClick={() => setCollapsed(!collapsed)}
                className="p-1 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 w-full flex justify-end"
              >
                {collapsed ? (
                  <ChevronRight size={20} />
                ) : (
                  <ChevronLeft size={20} />
                )}
              </button>
            )}
          </div>

          {/* New Chat Button */}
          <button
            onClick={handleNewChat}
            className={`flex items-center px-4 py-2 mb-4 text-sm font-medium rounded-md transition-all duration-200 ${
              collapsed && !isMobile
                ? "justify-center px-2 bg-transparent"
                : "bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:from-blue-600 hover:to-purple-700 transform hover:scale-105"
            }`}
            title="New Chat"
          >
            {collapsed && !isMobile ? (
              <span className="whitespace-nowrap bg-white shadow-lg rounded-full p-2 flex items-center justify-center">
                <Plus size={22} className="text-blue-500" />
              </span>
            ) : (
              <>
                <Plus size={20} className="mr-3" />
                <span>New Chat</span>
              </>
            )}
          </button>

          <nav className="space-y-1 flex-grow">
            {links.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`flex items-center px-4 py-2 text-sm font-medium rounded-md ${
                  isActive(link.path)
                    ? "bg-[#0f25636c] text-white"
                    : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                } ${collapsed && !isMobile ? "justify-center px-2" : ""}`}
                title={collapsed && !isMobile ? link.label : ""}
              >
                <span className={collapsed && !isMobile ? "" : "mr-3"}>
                  {link.icon}
                </span>
                {(!collapsed || isMobile) && link.label}
              </Link>
            ))}
          </nav>

          {/* Mobile Menu Button (shown at the bottom on desktop when collapsed) */}
          {!isMobile && collapsed && (
            <button
              onClick={() => setCollapsed(false)}
              className="mt-4 p-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 flex justify-center"
            >
              <Menu size={20} />
            </button>
          )}
        </div>
      </aside>
    </>
  );
}

export default Sidebar;
