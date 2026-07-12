function Button({

  children,

  onClick,

  className = "",

  disabled = false

}) {

  return (

    <button

      className={className}

      onClick={onClick}

      disabled={disabled}

    >

      {children}

    </button>

  );

}

export default Button;