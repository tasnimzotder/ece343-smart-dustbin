import { SiGithub } from 'react-icons/si';

const Footer = () => {
  return (
    <footer className="bg-gray-300 py-6 px-3 flex flex-col gap-4 items-center">
      <p className="text-xl">
        <a
          href="https://github.com/tasnimzotder/ece343-smart-dustbin"
          target="_blank"
          rel="noopener noreferrer"
        >
          <SiGithub />
        </a>
      </p>

      <p className="text-gray-700 text-sm">
        &copy; {new Date().getFullYear()} Smart Dustbin
      </p>
    </footer>
  );
};

export default Footer;
