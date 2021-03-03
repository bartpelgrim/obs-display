export const PigeonMarker = ({ left, top, style, onClick, children }) => (
  <div style={{
    position: 'absolute',
    left: left -20,
    top: top -20,
    width: 40,
    height: 40,
    borderTopLeftRadius: '100%',
    borderTopRightRadius: '100%',
    borderBottomLeftRadius: '100%',
    borderBottomRightRadius: '100%',
    background: 'red',
    fontSize: 20,
    ...(style || {})
  }} onClick={onClick}>
    {children}
  </div>
)

