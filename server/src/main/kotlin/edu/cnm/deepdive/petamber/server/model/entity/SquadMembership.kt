package edu.cnm.deepdive.petamber.server.model.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.FetchType
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import jakarta.persistence.Index
import jakarta.persistence.JoinColumn
import jakarta.persistence.ManyToOne
import jakarta.persistence.Table
import jakarta.persistence.UniqueConstraint
import org.hibernate.annotations.CreationTimestamp
import kotlin.time.Instant

@Entity
@Table(
    name = "squad_membership",
    uniqueConstraints = [
        UniqueConstraint(
            name = "uq_squad_membership_user_report",
            columnNames = ["user_id", "pet_report_id"]
        )
    ],
    indexes = [
        Index(columnList = "user_id"),
        Index(columnList = "pet_report_id")
    ]
)
class SquadMembership(

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false, updatable = false)
    var user: UserProfile,

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "pet_report_id", nullable = false, updatable = false)
    var petReport: PetReport,

    @Column(name = "is_active", nullable = false)
    var isActive: Boolean = true

) {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "squad_membership_id", nullable = false, updatable = false)
    var id: Long? = null

    @Column(nullable = false, updatable = false)
    @CreationTimestamp
    open var joined: Instant? = null

}
