--- script
print("example.lua -------------> hello there")

for i=0,255 do
  screen.pixel(i,10,0xFFFFFF-i);
  screen.pixel(i,20,0x00FFFF-i);
  screen.pixel(i,30,0xFF00FF-i);
end

screen.redraw()

key = function(x)
  screen.pixel(math.random(256),math.random(16)+50,0xFFFFFF);
  screen.redraw()
  osc.send({"127.0.0.1",57110},"/n",{x%127})
  print("key: "..x)
end

metro.tick = function(i,s)
  print("metro",i,s)
  grid.all(s)
  grid.redraw()
end

metro.start(1,0.1,5,0);

grid.key = function(x,y,z)
  print("grid",x,y,z)
  osc.send({"127.0.0.1",57110},"/n",{(7-y)*5+x+30})
  grid.led(x,y,15);
  grid.redraw();
end

dofile("test.lua")

