type NotificationProps = {
  nome: string;
  descricao: string;
  Icon?: any;
  size?: string;
  hidden?: boolean;
  color?: { bg: string; text: string };
  timeout?: number | null;
};
