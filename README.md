# CraigRenyolds-SteeringBehaviours
Creating an autonomous vehicle based on the rules by Craig W. Reynolds 
based on the paper Steering Behaviors For Autonomous Characters written by Craig W. Reynolds.

http://www.red3d.com/cwr/steer/gdc99/

# Implementation

Steering Behaviors For Autonomous Characters implemented in python using Pygame.
System uses vector maths to create parameters for vehicles which we use to manipulate the vehicle if implemented behaviors.


# Currently implemented behaviours

Seek
- Vehicle seeks and intercepts target vector (defined as a position) 
- Vehicle will try to move at full speed towards given target.

Flee
- Opposite of Seek; Vehicle will move directly away, at full speed, from given target vector

Pursue
- Seek a moving target ( potentially another vehicle )
- will intercept target based on own self max speed, targets velocity using law of sines.
- ( rudermentry pursue also included showing progession of behaviors )

Arrive
- Vehicle will Seek target and slow its velocity to arrive directly on top of target.
- Will slow down linearly based on vehicles propertys to correctly arrive at target ( Mass, Max speed and Max force )

Wander
- Move around the surface in a random direction by taking the last random wander position and randomising from there.
- creates a smooth wandering pattern that doesnt display random jitters

Follow Path ( Currently not fully implemented ) 
- vehicle follows a path ( created from a path object ) 
- uses scalar projection to move along the path in a fluid way.

To be implemented:

- obstical avoidence
- follow field
- unaligned collision avoidence
- neighbouring vehicles
- vehicle seperation
- vehicle cohesion
- vehicle alighnment
- vehicle leader follow
