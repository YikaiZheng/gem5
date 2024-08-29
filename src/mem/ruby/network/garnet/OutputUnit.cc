/*
 * Copyright (c) 2020 Inria
 * Copyright (c) 2016 Georgia Institute of Technology
 * Copyright (c) 2008 Princeton University
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */


#include "mem/ruby/network/garnet/OutputUnit.hh"

#include "debug/RubyNetwork.hh"
#include "mem/ruby/network/garnet/Credit.hh"
#include "mem/ruby/network/garnet/CreditLink.hh"
#include "mem/ruby/network/garnet/Router.hh"
#include "mem/ruby/network/garnet/flitBuffer.hh"

namespace gem5
{

namespace ruby
{

namespace garnet
{

OutputUnit::OutputUnit(int id, PortDirection direction, Router *router,
  uint32_t consumerVcs)
  : Consumer(router), m_router(router), m_id(id), m_direction(direction),
    m_vc_per_vnet(consumerVcs)
{
    const int m_num_vcs = consumerVcs * m_router->get_num_vnets();
    outVcState.reserve(m_num_vcs);
    for (int i = 0; i < m_num_vcs; i++) {
        outVcState.emplace_back(i, m_router->get_net_ptr(), consumerVcs);
    }
}

void
OutputUnit::decrement_credit(int out_vc)
{
    DPRINTF(RubyNetwork, "Router %d OutputUnit %s decrementing credit:%d for "
            "outvc %d at time: %lld for %s\n", m_router->get_id(),
            m_router->getPortDirectionName(get_direction()),
            outVcState[out_vc].get_credit_count(),
            out_vc, m_router->curCycle(), m_credit_link->name());

    outVcState[out_vc].decrement_credit();
}

void
OutputUnit::increment_credit(int out_vc)
{
    DPRINTF(RubyNetwork, "Router %d OutputUnit %s incrementing credit:%d for "
            "outvc %d at time: %lld from:%s\n", m_router->get_id(),
            m_router->getPortDirectionName(get_direction()),
            outVcState[out_vc].get_credit_count(),
            out_vc, m_router->curCycle(), m_credit_link->name());

    outVcState[out_vc].increment_credit();
}

// Check if the output VC (i.e., input VC at next router)
// has free credits (i..e, buffer slots).
// This is tracked by OutVcState
bool
OutputUnit::has_credit(int out_vc)
{
    if (!m_router->get_wormhole_enabled()){
        assert(outVcState[out_vc].isInState(ACTIVE_, curTick()));
    }
    return outVcState[out_vc].has_credit();
}


// Check if the output port (i.e., input port at next router) has free VCs.
bool
OutputUnit::has_free_vc(int vnet)
{
    int vc_base = vnet*m_vc_per_vnet;
    for (int vc = vc_base; vc < vc_base + m_vc_per_vnet; vc++) {
        if (m_router->get_wormhole_enabled()){
            if (outVcState[vc].has_credit()){
                return true;
            }
        }
        else{
            if (is_vc_idle(vc, curTick()))
                return true;
        }
    }

    return false;
}

int 
OutputUnit::count_free_vc(int vnet)
{
    int vc_base = vnet*m_vc_per_vnet;
    int num = 0;
    for (int vc = vc_base; vc < vc_base + m_vc_per_vnet; vc++) {
        if (m_router->get_wormhole_enabled()){
            if (outVcState[vc].has_credit()){
                num++;
            }
        }
        else{
            if (is_vc_idle(vc, curTick()))
                num++;
        }
    }
    return num;
}

// Escape VC
bool
OutputUnit::has_free_vc(int vnet, bool escape_vc_available, PortDirection outport_dirn, RouteInfo route)
{
    RoutingAlgorithm routing_algorithm =
        (RoutingAlgorithm) m_router->get_net_ptr()->getRoutingAlgorithm();

    if (routing_algorithm == ESCAPE_VC_ || routing_algorithm == ESCAPE_VC_ADAPTIVE_ || routing_algorithm == ESCAPE_VC_DOUBLE_ || (routing_algorithm == BUBBLE_DOUBLE_ && outport_dirn == "Across")){
        int vc_base = vnet*m_vc_per_vnet;
        for (int vc = escape_vc_available ? vc_base : vc_base + 1; vc < vc_base + m_vc_per_vnet; vc++) {
            if (m_router->get_wormhole_enabled()){
                if (outVcState[vc].has_credit()){
                    return true;
                }
            }
            else{
                if (is_vc_idle(vc, curTick()))
                    return true;
            }
        }
        return false;
    }
    return OutputUnit::has_free_vc(vnet);
}

int
OutputUnit::count_free_vc(int vnet, bool escape_vc_available, PortDirection outport_dirn, RouteInfo route)
{
    RoutingAlgorithm routing_algorithm =
        (RoutingAlgorithm) m_router->get_net_ptr()->getRoutingAlgorithm();
    int num = 0;

    if (routing_algorithm == ESCAPE_VC_ || routing_algorithm == ESCAPE_VC_ADAPTIVE_ || routing_algorithm == ESCAPE_VC_DOUBLE_ || (routing_algorithm == BUBBLE_DOUBLE_ && outport_dirn == "Across")){
        int vc_base = vnet*m_vc_per_vnet;
        for (int vc = escape_vc_available ? vc_base : vc_base + 1; vc < vc_base + m_vc_per_vnet; vc++) {
            if (m_router->get_wormhole_enabled()){
                if (outVcState[vc].has_credit()){
                    num++;
                }
            }
            else{
                if (is_vc_idle(vc, curTick()))
                    num++;
            }
        }
        return num;
    }
    return OutputUnit::count_free_vc(vnet);
}

int
OutputUnit::num_free_vc(int vnet)
{
    int vc_base = vnet*m_vc_per_vnet;
    int num = 0;
    for (int vc = vc_base; vc < vc_base + m_vc_per_vnet; vc++) {
        if (is_vc_idle(vc, curTick())){
            num++;
        }
    }
    return num;
}

// Assign a free output VC to the winner of Switch Allocation
//TODO: modify the check for free vc

int
OutputUnit::select_free_vc(int vnet)
{
    int vc_base = vnet*m_vc_per_vnet;
    for (int vc = vc_base; vc < vc_base + m_vc_per_vnet; vc++) {
        if (m_router->get_wormhole_enabled()){
            if (outVcState[vc].has_credit()){
                return vc;
            }
        }
        else{
            if (is_vc_idle(vc, curTick())) {
                outVcState[vc].setState(ACTIVE_, curTick());
                return vc;
            }
        }
    }

    return -1;
}

int
OutputUnit::select_free_vc(int vnet, bool escape_vc_available, PortDirection outport_dirn, RouteInfo route)
{
    RoutingAlgorithm routing_algorithm =
        (RoutingAlgorithm) m_router->get_net_ptr()->getRoutingAlgorithm();

    if (routing_algorithm == ESCAPE_VC_ || routing_algorithm == ESCAPE_VC_ADAPTIVE_ || routing_algorithm == ESCAPE_VC_DOUBLE_ || (routing_algorithm == BUBBLE_DOUBLE_ && outport_dirn == "Across")){
        int vc_base = vnet*m_vc_per_vnet;
        for (int vc = escape_vc_available ? vc_base : vc_base + 1; vc < vc_base + m_vc_per_vnet; vc++) {
            if (m_router->get_wormhole_enabled()){
                if (outVcState[vc].has_credit()){
                    return vc;
                }
            }
            else{
                if (is_vc_idle(vc, curTick())) {
                    outVcState[vc].setState(ACTIVE_, curTick());
                    return vc;
                }
            }
        }
        return -1;
    }
    return OutputUnit::select_free_vc(vnet);
}

/*
 * The wakeup function of the OutputUnit reads the credit signal from the
 * downstream router for the output VC (i.e., input VC at downstream router).
 * It increments the credit count in the appropriate output VC state.
 * If the credit carries is_free_signal as true,
 * the output VC is marked IDLE.
 */

//TODO: check how to set vc state in wakeup function

void
OutputUnit::wakeup()
{
    if (m_credit_link->isReady(curTick())) {
        // process credit
        Credit *t_credit = (Credit*) m_credit_link->consumeLink();
        increment_credit(t_credit->get_vc());
        if (!m_router->get_wormhole_enabled()){
            if (t_credit->is_free_signal())
                set_vc_state(IDLE_, t_credit->get_vc(), curTick());
        }

        delete t_credit;

        if (m_credit_link->isReady(curTick())) {
            scheduleEvent(Cycles(1));
        }
    }
}

flitBuffer*
OutputUnit::getOutQueue()
{
    return &outBuffer;
}

void
OutputUnit::set_out_link(NetworkLink *link)
{
    m_out_link = link;
}

void
OutputUnit::set_credit_link(CreditLink *credit_link)
{
    m_credit_link = credit_link;
}

void
OutputUnit::insert_flit(flit *t_flit)
{
    outBuffer.insert(t_flit);
    m_out_link->scheduleEventAbsolute(m_router->clockEdge(Cycles(1)));
}

bool
OutputUnit::functionalRead(Packet *pkt, WriteMask &mask)
{
    return outBuffer.functionalRead(pkt, mask);
}

uint32_t
OutputUnit::functionalWrite(Packet *pkt)
{
    return outBuffer.functionalWrite(pkt);
}

} // namespace garnet
} // namespace ruby
} // namespace gem5
